"""Datos de entrada: AUM al cierre de año (miles de millones USD) y eventos.

Las cifras de AUM provienen de resúmenes de búsqueda web que citan 10-K/8-K de la
SEC, Pensions & Investments, advratings, MarketsWiki y Bogleheads. No se pudieron
abrir las fuentes primarias desde este entorno: tratar como NO VERIFICADAS.
"""

FIRMS = {
    "BlackRock": {
        "profile": "World's largest asset manager; dominated by index funds and iShares ETFs; grew partly through acquisitions (MLIM 2006, BGI/iShares 2009).",
        "aum": {2005: 453, 2007: 1357, 2008: 1307, 2009: 3346, 2010: 3561, 2011: 3513,
                2012: 3792, 2013: 4324, 2014: 4652, 2015: 4645, 2016: 5148, 2017: 6288,
                2018: 5976, 2019: 7430, 2020: 8677, 2021: 10010, 2022: 8594, 2023: 10009,
                2024: 11551},
    },
    "Vanguard": {
        "profile": "Client-owned manager focused on low-cost index mutual funds and ETFs; grows almost entirely organically through net inflows.",
        "aum": {2005: 1000, 2010: 1600, 2015: 3400, 2017: 4900, 2018: 5000, 2019: 6200,
                2020: 7100, 2021: 8500, 2022: 7200, 2023: 8600, 2024: 10000},
    },
    "State Street Global Advisors": {
        "profile": "Asset management arm of State Street bank; large institutional index business and SPDR ETFs (including SPY).",
        "aum": {2007: 1980, 2008: 1440, 2015: 2245, 2021: 4140, 2022: 3500, 2023: 4100, 2024: 4700},
    },
    "Blackstone": {
        "profile": "Largest alternative asset manager: private equity, real estate, private credit, hedge fund solutions; IPO in 2007; AUM grows through fundraising and deployment into illiquid private assets.",
        "aum": {2007: 102.4, 2010: 128.1, 2015: 336.4, 2019: 571.1, 2021: 880.9, 2022: 974.7,
                2023: 1040.2, 2024: 1127.2},
    },
}

# (año_inicio, año_fin, descripción) — conocimiento histórico general, no cifras.
EVENTS = [
    (2007, 2009, "Global financial crisis: US subprime collapse, Lehman Brothers bankruptcy (Sep 2008), global equity crash, bank bailouts."),
    (2008, 2014, "Fed cuts rates to near zero and runs quantitative easing (QE1-QE3); investors search for yield."),
    (2009, 2009, "BlackRock acquires Barclays Global Investors (BGI) including iShares ETFs."),
    (2010, 2012, "Eurozone sovereign debt crisis (Greece, Ireland, Portugal, Spain, Italy); ECB 'whatever it takes' in 2012."),
    (2010, 2010, "Dodd-Frank Act in the US; Volcker rule limits banks' proprietary trading and fund ownership."),
    (2011, 2011, "US credit rating downgrade by S&P; sharp market sell-off in August."),
    (2015, 2016, "China stock crash and yuan devaluation; oil price collapse; Brexit vote (Jun 2016); Trump election (Nov 2016)."),
    (2017, 2017, "Low-volatility global equity rally; US tax cuts passed in December."),
    (2018, 2018, "Fed rate hikes and balance-sheet runoff; US-China trade war; Q4 equity sell-off."),
    (2019, 2019, "Fed pivots to rate cuts; strong equity and bond rally."),
    (2020, 2020, "COVID-19 pandemic: market crash in March, then massive fiscal stimulus and Fed QE drive a fast recovery."),
    (2021, 2021, "Stimulus-fueled boom: record equity highs, retail investing surge, record private-market fundraising."),
    (2022, 2022, "Inflation surge, fastest Fed hiking cycle in decades, Russia invades Ukraine; stocks and bonds fall together."),
    (2023, 2023, "US regional bank failures (SVB, March); AI-driven tech rally; rates stay high."),
    (2024, 2024, "Fed begins cutting rates; equity rally led by large tech; US presidential election."),
]
