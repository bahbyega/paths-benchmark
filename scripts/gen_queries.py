import numpy, sys, os, shutil

templates = [
    (1, "%s*", "q1"),
    (2, "%s %s*", "q2"),
    (3, "%s %s* %s*", "q3"),
    (2, "(%s | %s)*", "q4_2"),
    (3, "(%s | %s | %s)*", "q4_3"),
    (4, "(%s | %s | %s | %s)*", "q4_4"),
    (5, "(%s | %s | %s | %s | %s)*", "q4_5"),
    (3, "%s %s* %s", "q5"),
    (2, "%s* %s*", "q6"),
    (3, "%s %s %s*", "q7"),
    (2, "%s? %s*", "q8"),
    (2, "(%s | %s)+", "q9_2"),
    (3, "(%s | %s | %s)+", "q9_3"),
    (4, "(%s | %s | %s | %s)+", "q9_4"),
    (5, "(%s | %s | %s | %s | %s)+", "q9_5"),
    (3, "(%s | %s) %s*", "q10_2"),
    (4, "(%s | %s | %s) %s*", "q10_3"),
    (5, "(%s | %s | %s | %s) %s*", "q10_4"),
    (6, "(%s | %s | %s | %s | %s) %s*", "q10_5"),
    (2, "%s %s", "q11_2"),
    (3, "%s %s %s", "q11_3"),
    (4, "%s %s %s %s", "q11_4"),
    (5, "%s %s %s %s %s", "q11_5"),
    (4, "((%s %s)+) | (%s %s)+", "q12"),
    (5, "((%s (%s %s)*)+) | (%s %s)+", "q13"),
    (6, "((%s %s (%s %s)*)+) | (%s | %s)*", "q14"),
    (4, "(%s | %s)+ (%s | %s)+", "q15"),
    (5, "%s %s (%s | %s | %s)", "q16"),
]


def gen(tpl, n, lst, k):
    res = set()
    i = 0
    while len(res) < n:
        ie += 1
        perm = numpy.random.permutation(lst)
        res.add(((tpl % tuple(perm[0:k])), tuple(perm[0:k])))
        if i > 100:
            break
    return res


def gen_from_config(config, num_of_labels, num_of_queries):
    lbls = [
        l.split(" ")[0].rstrip() for l in open(config, "r").readlines()
    ]  # [0] if labels, [1] if label nums
    # print(lbls)
    enough_lbls = num_of_labels - len(lbls)
    if enough_lbls > 0:
        for i in range(enough_lbls):
            lbls.append(lbls[0])
    return [
        (tpl[2], gen(tpl[1], num_of_queries, lbls[0:num_of_labels], tpl[0]))
        for tpl in templates
    ]


def write_qs(qs, root_dir, form):
    for qd in qs:
        path = os.path.join(root_dir, qd[0])
        if os.path.exists(path):
            shutil.rmtree(path)
        os.mkdir(path)
        i = 0
        for q in qd[1]:
            with open(os.path.join(path, str(i)), "w") as out:
                if form == "regex":
                    out.write(q[0] + "\n")
                elif form == "grammar":
                    out.write("S -> " + q[0] + "\n")
                else:
                    print(f"Error: invalid form:{form}")
                i = i + 1


def gen_qs(path_to_config, num_labels, count, path_to_qs, form, seed):
    numpy.random.seed(seed)

    # print("Generating queries")
    # print(path_to_config, num_labels,int(count))
    r = gen_from_config(path_to_config, num_labels, count)

    write_qs(r, path_to_qs, form)
