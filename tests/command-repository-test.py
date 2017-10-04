import unittest

from prjrepo.workflow.repository import DefaultCommandRepository


COMMAND_DIR = './.prm/commands'


class TestCommandRepository(unittest.TestCase):

    def setUp(self):
        """Initialize the command repository manager."""
        self.repo = DefaultCommandRepository(COMMAND_DIR)

    def test_list_commands(self):
        """Test listing of registered commands."""
        commands = self.repo.list_commands()
        self.assertTrue('list-datasets' in commands)
        self.assertTrue('run-java' in commands)

    def test_list_dataset_command(self):
        """Command to execute SQL query that lists datasets."""
        cmd = self.repo.get_command('list-datasets')
        self.assertTrue(cmd.is_sql)
        self.assertEquals(cmd.name, 'list-datasets')
        self.assertEquals(len(cmd.components), 2)
        self.assertTrue(cmd.components[0].is_const)
        self.assertTrue(cmd.components[1].is_var)

    def test_run_java_command(self):
        """Command to execute Java Jar file."""
        cmd = self.repo.get_command('run-java')
        self.assertTrue(cmd.is_exec)
        self.assertEquals(cmd.name, 'run-java')
        self.assertEquals(len(cmd.components), 3)
        self.assertTrue(cmd.components[1].as_input)
        self.assertTrue(cmd.components[0].is_const)
        self.assertTrue(cmd.components[1].is_var)
        self.assertTrue(cmd.components[1].ref_io)
        self.assertTrue(cmd.components[1].ref_file)
        self.assertTrue(cmd.components[1].as_input)
        self.assertFalse(cmd.components[1].ref_dir)
        self.assertTrue(cmd.components[2].is_const)
        self.assertFalse(cmd.components[2].ref_io)
        self.assertFalse(cmd.components[2].ref_file)
        self.assertFalse(cmd.components[2].ref_dir)
        self.assertFalse(cmd.components[2].as_input)


if __name__ == '__main__':
    unittest.main()
