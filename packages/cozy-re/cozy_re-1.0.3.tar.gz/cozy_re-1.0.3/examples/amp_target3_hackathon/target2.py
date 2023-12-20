import angr
import cozy
import archinfo

arch = archinfo.arch_pcode.ArchPcode('sparc:BE:32:default')
arch.stack_change = -4

def run_prepatch():
    prepatch_proj = cozy.project.Project('sphinx_vuln', arch=arch)
    prepatch_proj.add_prototype('get_temp', 'void *get_temp(void *)')
    prepatch_sess = prepatch_proj.session('get_temp')
    return (prepatch_proj.object_ranges(), prepatch_sess.run(0x0))

def run_postpatch():
    postpatch_proj = cozy.project.Project('sphinx_good', arch=arch)
    postpatch_proj.add_prototype('get_temp', 'void *get_temp(void *)')
    postpatch_sess = postpatch_proj.session('get_temp')
    return (postpatch_proj.object_ranges(), postpatch_sess.run(0x0))

(pre_code_ranges, pre_patched) = run_prepatch()
(post_code_ranges, post_patched) = run_postpatch()

prog_addrs = pre_code_ranges + post_code_ranges
comparison_results = cozy.analysis.Comparison(pre_patched, post_patched, prog_addrs)

print(comparison_results.report([]))