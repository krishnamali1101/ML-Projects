from pylint import epylint as lint
(pylint_stdout, pylint_stderr) = lint.py_run('doc2vec_gensim.py', return_std=True)
print(pylint_stderr, pylint_stdout)