(lambda d, p, s: (
    (lambda l:(
        [
            [
                (lambda x, t: (
                    p.subplots(),
                    print(sorted(x), t),
                    p.scatter(x, [x.count(x[i]) for i in range(len(x))], s=5),
                    [
                        p.plot([
                            x[b]-.33, 
                            x[b]+.33, 
                            x[b]+.33, 
                            x[b]-.33,
                            x[b]-.33
                        ], [
                            0, 
                            0,
                            x.count(x[b]), 
                            x.count(x[b]), 
                            0
                        ], 'k-') for b in range(len(x))
                    ],
                    [
                        p.fill_between([
                            x[b]-.33, 
                            x[b]+.33, 
                            x[b]+.33, 
                            x[b]-.33,
                            x[b]-.33
                        ], [
                            0, 
                            0, 
                            x.count(x[b]), 
                            x.count(x[b]), 
                            0
                        ], alpha=.5, color='orange') for b in range(len(x))
                    ],
                    p.xlabel('Value'),
                    p.ylabel('Density'),
                    p.title(f'{t} - Score Density Plot'),
                    p.grid(True),
                    p.savefig(f'figs/{t}_Density')
                ))(t[1][:-2], t[0])
                for t in l
            ],
            p.pause(50)
        ] if '-p=d' in s else None, 
        [
            (
               lambda d, np: (
                (
                    boxplot_colors := [
                        'red' if len(values) > 0 and (
                            np.max(values) > np.percentile(values, 75) + 1.5 * (np.percentile(values, 75) - np.percentile(values, 25))
                            or np.min(values) < np.percentile(values, 25) - 1.5 * (np.percentile(values, 75) - np.percentile(values, 25))
                        ) else 'blue'
                        for title, values in d.items()
                    ],
                    p.subplots(),
                    [
                        p.boxplot(
                            values,
                            positions=[i + 1],
                            patch_artist=True,
                            vert=False,
                            widths = .75,
                            boxprops=dict(facecolor=color, linewidth=1),  
                            capprops=dict(color='black', linewidth=1),  
                            whiskerprops=dict(color='black', linewidth=1),  
                            medianprops=dict(color='black', linewidth=1),  
                            meanprops=dict(color='black', marker='D', markersize=1),  
                        )
                        for i, (title, values, color) in enumerate(zip(d.keys(), d.values(), boxplot_colors))
                    ],
                    p.xlabel('Score Distribution'),
                    p.ylabel('Major'),
                    p.title('Major Score Distribution Boxplot with Outlier Detection'),
                    p.yticks(range(1, len(d) + 1), d.keys()),
                    p.grid(True),
                    p.savefig('figs/boxplot'),
                    p.show(),
                )
            )
            )(
                {
                    t[0]: t[1][:-2]
                    for t in l 
                },
                __import__('numpy'),
            )
        ] if '-p=b' in s else None,
        [
            print(__import__('json').dumps(d))
        ] if '-j' in s else None,
        [
            (lambda x: (
                print({
                    k: v for k, v in x.items() 
                    if k not in s
                }), 
                print(
                    __import__(
                        'scipy.stats',
                        fromlist=['stats']
                    ).f_oneway(
                        *__import__('pandas').DataFrame({
                            k: v for k, v in x.items() 
                            if k not in s
                        }).values.T
                    )
                )
            ))({t[0]: t[1][:-2]for t in l})
        ] if '-m' in s else None,
        [ 
            print("Useage:"),
            print("-p=d: Plot density"),
            print("-p=b: Plot boxplots of major ratings"),
            print("-j:   Output json"),
            print("-m:   Perform ANOVA test"),
            print(
                "\twhen using -m, major names to exclude from the calculations may be passed, valid majors include:\n       ",
                "\n\t".join(list(d['1'].keys())[:-2])
            )
        ] if s[1:] == [] else None,
    ))(
        [
            (
                list(v.keys())[0], 
                *list(v.values())
            ) for v in [
                {key: 
                     [
                        f[key] for f in [
                            {
                                i: k[1][i] for i in k[1].keys() if i == v
                            } for k in zip(d.keys(), d.values())
                        ] if key in f
                    ] for key in set(
                        key for f in [
                            {
                                i: k[1][i] for i in k[1].keys() if i == v
                            } for k in zip(
                                d.keys(), 
                                d.values()
                            )
                        ] for key in f
                    )
                } for v in d['1'].keys() if v not in [
                    'Mean', 
                    'Std Dev'
                ]
            ]
        ]
    )
))(
    __import__('json').loads(
        (lambda d: (
            (lambda g, j: (
                __import__('json').dumps(
                    (lambda p: [
                        p.update(
                            {
                                "Mean": {
                                    g[i]: sum(
                                        [
                                            v for v in [p[k][g[i]] for k in p.keys()]
                                        ]
                                    )/len(
                                        p.keys()
                                    ) for i in range(len(g))
                                }, 
                                "Std Dev": {
                                    g[i]: __import__('statistics').stdev(
                                        [
                                            v for v in [p[k][g[i]] for k in p.keys()]
                                        ]
                                    ) for i in range(len(g))
                                }
                            }
                        ),
                        p
                    ][1])(
                        dict(
                            zip(
                                range(1, j.index(['']*10) + 1),
                                [
                                    {
                                        **{g[k]: list(
                                            map(
                                                lambda x: int(x) if x else 0, 
                                                filter(
                                                    lambda x: j[i].index(x) < j.index(['']*10), 
                                                    j[i]
                                                )
                                            )
                                        )[k] for k in range(len(g))},
                                        **{"Mean": sum(
                                            map(
                                                lambda x: int(x) if x else 0, 
                                                j[i]
                                            )
                                        )/len(j[i]), 
                                        "Std Dev": __import__("statistics").stdev(
                                            map(
                                                lambda x: int(x) if x else 0, 
                                                j[i]
                                            )
                                        )}
                                    } for i in range(
                                        j.index(['']*10)
                                    )
                                ]
                            )
                        )
                    )
                )
            ))( 
                d.split('\n')[0].split(',')[1:],
                list(
                    map(
                        lambda x: x.split(',')[1:],
                        d.split('\n')[1:]
                    )
                )
            )
        )
    )(
    [(f:=open('data.csv', 'r')).read(), f.close()][0])),
    __import__('matplotlib.pyplot', fromlist=['pyplot']),
    __import__('sys').argv
)

