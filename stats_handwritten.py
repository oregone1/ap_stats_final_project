(lambda d, p, s: (
    (lambda l:(
        [
            [
                (lambda x, t: (
                    ax:=p.subplots(figsize=(5.1, 2.3)),
                    print(sorted(x[:-2]), t),
                    ax[1].scatter(x[:-2], [x[:-2].count(x[:-2][i]) for i in range(len(x[:-2]))], s=5),
                    [
                        ax[1].plot([
                            x[:-2][b]-.33, 
                            x[:-2][b]+.33, 
                            x[:-2][b]+.33, 
                            x[:-2][b]-.33,
                            x[:-2][b]-.33
                        ], [
                            0, 
                            0,
                            x[:-2].count(x[:-2][b]), 
                            x[:-2].count(x[:-2][b]), 
                            0
                        ], 'k-') for b in range(len(x[:-2]))
                    ],
                    [
                        ax[1].fill_between([
                            x[:-2][b]-.33, 
                            x[:-2][b]+.33, 
                            x[:-2][b]+.33, 
                            x[:-2][b]-.33,
                            x[:-2][b]-.33
                        ], [
                            0, 
                            0, 
                            x[:-2].count(x[:-2][b]), 
                            x[:-2].count(x[:-2][b]), 
                            0
                        ], alpha=.5, color='orange') for b in range(len(x[:-2]))
                    ],
                    ax[1].set_aspect(1/2.5),
                    ax[1].text(0.05, 0.95, f"Mean: {x[-2]:.2f}", color='blue', ha='left', va='top', transform=p.gca().transAxes),
                    ax[1].text(0.05, 0.85, f"Median: {sorted(x[:-2])[len(x[:-2])//2] if len(x[:-2]) % 2 != 0 else sum(sorted(x[:-2])[len(x[:-2])//2-1:len(x[:-2])//2+1])/2:.2f}", color='red', ha='left', va='top', transform=p.gca().transAxes),
                    ax[1].text(0.05, 0.75, f"Std Dev: {x[-1]:.2f}", color='green', ha='left', va='top', transform=p.gca().transAxes),
                    p.subplots_adjust(left=.15, right=.95, bottom=.2, top=.9),
                    p.xlabel('Value'),
                    p.ylabel('Frequency'),
                    p.ylim(0, max(x)+1),
                    p.title(f'{t} - Score Density Plot'),
                    p.savefig(f'figs/{t}_Density')
                ))(t[1], t[0])
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
                    p.subplots(figsize=(10, 8)),
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

