import hashlib
import json
import os
import tempfile
import unittest

from alertmanager import AlertManager
from baselinemanager import BaselineManager
from filehasher import FileHasher
from filescanner import FileScanner


class TestFileHasher(unittest.TestCase):
    def setUp(self):
        self.hasher = FileHasher()
        self.tmp = tempfile.NamedTemporaryFile(delete=False)
        self.tmp.write(b'hello world')
        self.tmp.close()

    def tearDown(self):
        os.unlink(self.tmp.name)

    def test_calculate_hash_returns_sha256(self):
        expected = hashlib.sha256(b'hello world').hexdigest()
        self.assertEqual(self.hasher.calculate_hash(self.tmp.name), expected)

    def test_calculate_hash_on_directory_returns_none(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertIsNone(self.hasher.calculate_hash(d))

    def test_verify_hash_correct(self):
        expected = hashlib.sha256(b'hello world').hexdigest()
        self.assertTrue(self.hasher.verify_hash(self.tmp.name, expected))

    def test_verify_hash_incorrect(self):
        self.assertFalse(self.hasher.verify_hash(self.tmp.name, 'badhash'))

    def test_verify_hash_on_directory_returns_false(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertFalse(self.hasher.verify_hash(d, 'anyhash'))


class TestFileScanner(unittest.TestCase):
    def setUp(self):
        self.scanner = FileScanner()

    def test_returns_full_paths(self):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, 'file.txt')
            open(path, 'w').close()
            results = self.scanner.scan_directory(d)
            self.assertIn(path, results)

    def test_excludes_excluded_dirs(self):
        with tempfile.TemporaryDirectory() as d:
            git_dir = os.path.join(d, '.git')
            os.mkdir(git_dir)
            open(os.path.join(git_dir, 'HEAD'), 'w').close()
            results = self.scanner.scan_directory(d)
            self.assertFalse(any('.git' in p for p in results))

    def test_excludes_excluded_files(self):
        with tempfile.TemporaryDirectory() as d:
            open(os.path.join(d, 'baseline.json'), 'w').close()
            open(os.path.join(d, 'fim.log'), 'w').close()
            open(os.path.join(d, 'keep.txt'), 'w').close()
            results = self.scanner.scan_directory(d)
            names = [os.path.basename(p) for p in results]
            self.assertNotIn('baseline.json', names)
            self.assertNotIn('fim.log', names)
            self.assertIn('keep.txt', names)

    def test_recurses_subdirectories(self):
        with tempfile.TemporaryDirectory() as d:
            sub = os.path.join(d, 'sub')
            os.mkdir(sub)
            path = os.path.join(sub, 'file.txt')
            open(path, 'w').close()
            results = self.scanner.scan_directory(d)
            self.assertIn(path, results)


class TestBaselineManager(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.NamedTemporaryFile(suffix='.json', delete=False)
        self.tmp.close()
        os.unlink(self.tmp.name)
        self.manager = BaselineManager(baseline_path=self.tmp.name)

    def tearDown(self):
        if os.path.exists(self.tmp.name):
            os.unlink(self.tmp.name)

    def test_load_baseline_returns_none_when_missing(self):
        self.assertIsNone(self.manager.load_baseline())

    def test_save_and_load_roundtrip(self):
        baseline = {'file.txt': 'abc123'}
        self.manager.save_baseline(baseline)
        self.assertEqual(self.manager.load_baseline(), baseline)

    def test_compare_added(self):
        result = self.manager.compare({}, {'new.txt': 'hash1'})
        self.assertEqual(result['added'], {'new.txt': 'hash1'})
        self.assertEqual(result['removed'], {})
        self.assertEqual(result['modified'], {})

    def test_compare_removed(self):
        result = self.manager.compare({'old.txt': 'hash1'}, {})
        self.assertEqual(result['removed'], {'old.txt': 'hash1'})
        self.assertEqual(result['added'], {})
        self.assertEqual(result['modified'], {})

    def test_compare_modified(self):
        result = self.manager.compare({'f.txt': 'old'}, {'f.txt': 'new'})
        self.assertEqual(result['modified'], {'f.txt': {'baseline': 'old', 'current': 'new'}})
        self.assertEqual(result['added'], {})
        self.assertEqual(result['removed'], {})

    def test_compare_no_changes(self):
        scan = {'f.txt': 'hash1'}
        result = self.manager.compare(scan, scan)
        self.assertFalse(any(result.values()))


class TestAlertManager(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.NamedTemporaryFile(suffix='.log', delete=False)
        self.tmp.close()
        self.manager = AlertManager(log_path=self.tmp.name)

    def tearDown(self):
        os.unlink(self.tmp.name)

    def test_send_alert_writes_to_log(self):
        self.manager.send_alert('added', '/some/file.txt')
        with open(self.tmp.name) as f:
            content = f.read()
        self.assertIn('ADDED', content)
        self.assertIn('/some/file.txt', content)

    def test_send_alert_uppercases_change_type(self):
        self.manager.send_alert('modified', '/some/file.txt')
        with open(self.tmp.name) as f:
            content = f.read()
        self.assertIn('MODIFIED', content)

    def test_process_changes_dispatches_all(self):
        changes = {
            'added':    {'a.txt': 'h1'},
            'removed':  {'b.txt': 'h2'},
            'modified': {'c.txt': {'baseline': 'h3', 'current': 'h4'}},
        }
        self.manager.process_changes(changes)
        with open(self.tmp.name) as f:
            content = f.read()
        self.assertIn('ADDED', content)
        self.assertIn('REMOVED', content)
        self.assertIn('MODIFIED', content)

    def test_no_log_file(self):
        manager = AlertManager()
        manager.send_alert('added', '/file.txt')

    def test_process_changes_empty(self):
        self.manager.process_changes({'added': {}, 'removed': {}, 'modified': {}})
        with open(self.tmp.name) as f:
            self.assertEqual(f.read(), '')


if __name__ == '__main__':
    unittest.main()
