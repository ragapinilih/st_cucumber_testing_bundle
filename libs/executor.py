from libs.command import Command

class Executor(object):
  def __init__(self, job):
    self.job = job

  def _execute(self, command):
    print("Running command: {0}".format(command))
    self.job.window.run_command("exec", {
      "shell_cmd": command,
      "working_dir": self.job.root(),
    })

  def _line_number(self):
    return (str)(self.job.view.rowcol(self.job.view.sel()[0].begin())[0] + 1)

  def _prepare(self, file_name = None, line = None, tags = None):
    cmd_obj = Command(self.job)
    command = cmd_obj.retrieve(file_name, line, tags)

    cmd_obj.save(command)
    self._execute(command)

  def _run_file_with_tags(self, tags):
    self._prepare(self.job.view.file_name(), None, tags)

  def _run_tags(self, tags):
    self._prepare(None, None, tags)

  def run_cucumber(self):
    self._prepare()

  def run_current_file(self):
    self._prepare(self.job.view.file_name())

  def run_current_line(self):
    self._prepare(self.job.view.file_name(), self._line_number())

  def run_file_with_tags(self):
    self.job.window.show_input_panel(
      "Tags to run",
      self.job.get_tags(),
      self._run_file_with_tags,
      None,
      None
    )

  def run_last(self):
    self._execute(Command(self.job).last_command())

  def run_tags(self):
    self.job.window.show_input_panel(
      "Tags to run",
      self.job.get_tags(),
      self._run_tags,
      None,
      None
    )
