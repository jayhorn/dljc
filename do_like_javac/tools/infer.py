import argparse
import os
import pprint
import subprocess
import traceback

argparser = argparse.ArgumentParser(add_help=False)
infer_group = argparser.add_argument_group('inference tool arguments')

infer_group.add_argument('-s', '--solver', metavar='<solver>',
                         action='store', default='checkers.inference.solver.DebugSolver',
                         help='solver to use on constraints')
infer_group.add_argument('-afud', '--afuOutputDir', metavar='<afud>',
                         action='store', default='afud/',
                         help='Annotation File Utilities output directory')
infer_group.add_argument('-m', '--mode', metavar='<mode>',
                         action='store', default='INFER',
                         help='Modes of operation: TYPECHECK, INFER, ROUNDTRIP,ROUNDTRIP_TYPECHECK')


def run(args, javac_commands, jars):
	# the dist directory if CFI.
	CFI_dist = os.environ['JSR308'] + "/checker-framework-inference/dist"
	CFI_command = []

	CFI_command.extend(["java"])

	for jc in javac_commands:
		pprint.pformat(jc)
		javac_switches = jc['javac_switches']
		target_cp = javac_switches['classpath']
		java_files = ' '.join(jc['java_files'])
		cp = target_cp + ":" + CFI_dist + "/checker.jar:" + CFI_dist + "/plume.jar:" + \
		     CFI_dist + "/checker-framework-inference.jar"
		cmd = CFI_command + ["-classpath", cp, "checkers.inference.InferenceLauncher",
		                     "--checker", args.checker, "--solver", args.solver,
		                     "--mode", args.mode, "--targetclasspath", target_cp, "-afud", args.afuOutputDir,
		                     java_files]
		print ("Running %s" % cmd)
		try:
			print (subprocess.check_output(cmd, stderr=subprocess.STDOUT))
		except:
			print ('calling {cmd} failed\n{trace}'.format(cmd=' '.join(cmd), trace=traceback.format_exc()))
