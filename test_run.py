import run
import unittest


class TestRun(unittest.TestCase):
    def setUp(self):
        self.con = run.create_db()

    def tearDown(self):
        self.con.close()

    def query_one(self, query):
        cur = self.con.cursor()
        cur.execute(query)
        return cur.fetchone()

    def query_many(self, query):
        cur = self.con.cursor()
        cur.execute(query)
        return cur.fetchall()

    def test_import(self):
        run.run_import('example.sas7bdat', self.con)

        count = self.query_one('SELECT COUNT(*) FROM example')['COUNT(*)']
        self.assertEqual(count, 20)

        columns = self.query_many('PRAGMA TABLE_INFO(example)')
        column_types = {col['name']: col['type'] for col in columns}
        self.assertEqual(column_types['begin'], 'REAL')
        self.assertEqual(column_types['enddate'], 'TIMESTAMP')
        self.assertEqual(column_types['Info'], 'TEXT')
        self.assertEqual(column_types['year'], 'REAL')
        self.assertEqual(column_types['Capital'], 'REAL')
        self.assertEqual(column_types['YearFormatted'], 'REAL')

    def test_missing_src(self):
        with self.assertRaises(FileNotFoundError):
            run.run_import('nonexistent.sas7bdat', self.con)


if __name__ == '__main__':
    unittest.main()
