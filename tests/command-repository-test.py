import unittest

from prjrepo.command.repository import DefaultCommandRepository


COMMAND_DIR = './.prj/commands'


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
        self.assertEquals(len(cmd.elements), 2)

    def test_run_java_command(self):
        """Command to execute Java Jar file."""
        cmd = self.repo.get_command('run-java')
        self.assertTrue(cmd.is_exec)
        self.assertEquals(cmd.name, 'run-java')
        self.assertEquals(len(cmd.elements), 3)
        self.assertTrue(cmd.elements[1].is_input)


if __name__ == '__main__':
    unittest.main()
