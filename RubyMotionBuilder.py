import sublime, sublime_plugin
import os.path
import re

this_dir = os.path.split(os.path.abspath(__file__))[0]

def FindRubyMotionRakefile(dir_name):
	re_rubymotion = re.compile("Motion")
	while dir_name != "/":
		rakefile = os.path.join(dir_name, "Rakefile")
		if os.path.isfile(rakefile):
			for line in open(rakefile):
				if re_rubymotion.search(line):
					return dir_name
			return None
		dir_name = os.path.dirname(dir_name)
	return None

class RubyMotionBuild(sublime_plugin.WindowCommand):
	def run(self, build_target=None):
		view = self.window.active_view()
		if not view:
			return
		dir_name = FindRubyMotionRakefile(os.path.split(view.file_name())[0])
		if dir_name:
			sh_name = os.path.join(this_dir, "rubymotion_build.sh")
			cmd = "rake build"
			if build_target and build_target != "all":
				cmd += ":" + build_target
			file_regex = "^(...*?):([0-9]*):([0-9]*)"
			self.window.run_command("exec", {"cmd": ["sh", sh_name, cmd], "working_dir": dir_name, "file_regex": file_regex})

class RubyMotionClean(sublime_plugin.WindowCommand):
	def run(self):
		view = self.window.active_view()
		if not view:
			return
		dir_name = FindRubyMotionRakefile(os.path.split(view.file_name())[0])
		if dir_name:
			sh_name = os.path.join(this_dir, "rubymotion_build.sh")
			cmd = "rake clean"
			file_regex = "^(...*?):([0-9]*):([0-9]*)"
			self.window.run_command("exec", {"cmd": ["sh", sh_name, cmd], "working_dir": dir_name, "file_regex": file_regex})

class RubyMotionRun(sublime_plugin.WindowCommand):
	def run(self):
		view = self.window.active_view()
		if not view:
			return
		dir_name = FindRubyMotionRakefile(os.path.split(view.file_name())[0])
		if dir_name:
			sh_name = os.path.join(this_dir, "rubymotion_run.sh")
			file_regex = "^(...*?):([0-9]*):([0-9]*)"
			self.window.run_command("exec", {"cmd": ["sh", sh_name, dir_name], "working_dir": dir_name, "file_regex": file_regex})

class RubyMotionDeploy(sublime_plugin.WindowCommand):
	def run(self):
		view = self.window.active_view()
		if not view:
			return
		dir_name = FindRubyMotionRakefile(os.path.split(view.file_name())[0])
		if dir_name:
			sh_name = os.path.join(this_dir, "rubymotion_build.sh")
			cmd = "rake device"
			file_regex = "^(...*?):([0-9]*):([0-9]*)"
			self.window.run_command("exec", {"cmd": ["sh", sh_name, cmd], "working_dir": dir_name, "file_regex": file_regex})

class GenerateRubyMotionSyntax(sublime_plugin.WindowCommand):
	def run(self):
		rb_name = os.path.join(this_dir, "rubymotion_syntax_generator.rb")
		self.window.run_command("exec", {"cmd": ["ruby", rb_name], "working_dir": this_dir})

class GenerateRubyMotionCompletions(sublime_plugin.WindowCommand):
	def run(self):
		rb_name = os.path.join(this_dir, "rubymotion_completion_generator.rb")
		bridge_support_dir = "/Library/RubyMotion/data/5.1/BridgeSupport/"
		self.window.run_command("exec", {"cmd": ["ruby", rb_name, bridge_support_dir], "working_dir": this_dir})

class SetRubyMotionSyntax(sublime_plugin.EventListener):
	def on_load(self, view):
		dir_name, file_name = os.path.split(view.file_name())
		ext = os.path.splitext(file_name)[1]
		if ext == ".rb" or file_name == "Rakefile":
			if FindRubyMotionRakefile(dir_name):
				view.set_syntax_file(os.path.join(this_dir, "RubyMotion.tmLanguage"))

