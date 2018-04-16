import InputData as Settings
import scr.FormatFunctions as F
import scr.SamplePathClasses as PathCls
import scr.FigureSupport as Figs
import scr.StatisticalClasses as Stat
import scr.EconEvalClasses as Econ

def print_outcomes(simOutput, therapy_name):
    """ prints the outcomes of a simulated cohort
    :param simOutput: output of a simulated cohort
    :param therapy_name: the name of the selected therapy
    """
    # mean and confidence interval text of patient survival time
    survival_mean_CI_text = F.format_estimate_interval(
        estimate=simOutput.get_sumStat_survival_times().get_mean(),
        interval=simOutput.get_sumStat_survival_times().get_t_CI(alpha=Settings.ALPHA),
        deci=2)

    # mean and confidence interval text of time to stroke
    strokes_mean_CI_text = F.format_estimate_interval(
        estimate=simOutput.get_sumStat_count_strokes().get_mean(),
        interval=simOutput.get_sumStat_count_strokes().get_t_CI(alpha=Settings.ALPHA),
        deci=2)

    # print outcomes
    print(therapy_name)
    print("  Estimate of mean and {:.{prec}%} confidence interval of survival time:".format(1 - Settings.ALPHA, prec=0),
          survival_mean_CI_text)
    print("  Estimate of mean and {:.{prec}%} confidence interval of time to stroke:".format(1 - Settings.ALPHA, prec=0),
          strokes_mean_CI_text)
    print("")


def print_comparative_outcomes(simOutputs_mono, simOutputs_combo):
    """ prints average increase in survival time, discounted cost, and discounted utility
    under combination therapy compared to mono therapy
    :param simOutputs_mono: output of a cohort simulated under mono therapy
    :param simOutputs_combo: output of a cohort simulated under combination therapy
    """

    # increase in survival time under combination therapy with respect to mono therapy
    increase_survival_time = Stat.DifferenceStatIndp(
        name='Increase in survival time',
        x=simOutputs_combo.get_survival_times(),
        y_ref=simOutputs_mono.get_survival_times())

    # estimate and CI
    estimate_CI = F.format_estimate_interval(
        estimate=increase_survival_time.get_mean(),
        interval=increase_survival_time.get_t_CI(alpha=Settings.ALPHA),
        deci=2)
    print("Average increase in survival time "
          "and {:.{prec}%} confidence interval:".format(1 - Settings.ALPHA, prec=0),
          estimate_CI)

    # increase in discounted total cost under combination therapy with respect to mono therapy
    increase_discounted_cost = Stat.DifferenceStatIndp(
        name='Increase in discounted cost',
        x=simOutputs_combo.get_costs(),
        y_ref=simOutputs_mono.get_costs())

    # estimate and CI
    estimate_CI_cost= F.format_estimate_interval(
        estimate=increase_discounted_cost.get_mean(),
        interval=increase_discounted_cost.get_t_CI(alpha=Settings.ALPHA),
        deci=0,
        form=F.FormatNumber.CURRENCY)
    print("Average increase in discounted cost "
          "and {:.{prec}%} confidence interval:".format(1 - Settings.ALPHA, prec=0),
          estimate_CI_cost)

    # increase in discounted total utility under combination therapy with respect to mono therapy
    increase_discounted_utility = Stat.DifferenceStatIndp(
        name='Increase in discounted cost',
        x=simOutputs_combo.get_utilities(),
        y_ref=simOutputs_mono.get_utilities())

    # estimate and CI
    estimate_CI_utility = F.format_estimate_interval(
        estimate=increase_discounted_utility.get_mean(),
        interval=increase_discounted_utility.get_t_CI(alpha=Settings.ALPHA),
        deci=2)
    print("Average increase in discounted utility "
          "and {:.{prec}%} confidence interval:".format(1 - Settings.ALPHA, prec=0),
          estimate_CI_utility)


def report_CEA_CBA(simOutputs_mono, simOutputs_combo):
    """ performs cost-effectiveness and cost-benefit analyses
    :param simOutputs_mono: output of a cohort simulated under mono therapy
    :param simOutputs_combo: output of a cohort simulated under combination therapy
    """

    # define two strategies
    mono_therapy_strategy = Econ.Strategy(
        name='No Treatment',
        cost_obs=simOutputs_mono.get_costs(),
        effect_obs=simOutputs_mono.get_utilities()
    )
    combo_therapy_strategy = Econ.Strategy(
        name='With Treatment',
        cost_obs=simOutputs_combo.get_costs(),
        effect_obs=simOutputs_combo.get_utilities()
    )

    # do CEA
    CEA = Econ.CEA(
        strategies=[mono_therapy_strategy, combo_therapy_strategy],
        if_paired=False
    )
    # show the CE plane
    CEA.show_CE_plane(
        title='Cost-Effectiveness Analysis',
        x_label='Additional discounted utility',
        y_label='Additional discounted cost',
        show_names=True,
        show_clouds=True,
        show_legend=True,
        figure_size=6,
        transparency=0.3
    )
    # report the CE table
    CEA.build_CE_table(
        interval=Econ.Interval.CONFIDENCE,
        alpha=Settings.ALPHA,
        cost_digits=0,
        effect_digits=2,
        icer_digits=2,
    )

    # CBA
    NBA = Econ.CBA(
        strategies=[mono_therapy_strategy, combo_therapy_strategy],
        if_paired=False
    )
    # show the net monetary benefit figure
    NBA.graph_deltaNMB_lines(
        min_wtp=0,
        max_wtp=50000,
        title='Cost-Benefit Analysis',
        x_label='Willingness-to-pay for one additional QALY ($)',
        y_label='Incremental Net Monetary Benefit ($)',
        interval=Econ.Interval.CONFIDENCE,
        show_legend=True,
        figure_size=6
    )

    def report_CEA_CBA(simOutputs_mono, simOutputs_combo):
        """ performs cost-effectiveness and cost-benefit analyses
        :param simOutputs_mono: output of a cohort simulated under mono therapy
        :param simOutputs_combo: output of a cohort simulated under combination therapy
        """

        # define two strategies
        mono_therapy_strategy = Econ.Strategy(
            name='Mono Therapy',
            cost_obs=simOutputs_mono.get_costs(),
            effect_obs=simOutputs_mono.get_utilities()
        )
        combo_therapy_strategy = Econ.Strategy(
            name='Combination Therapy',
            cost_obs=simOutputs_combo.get_costs(),
            effect_obs=simOutputs_combo.get_utilities()
        )

        # do CEA
        CEA = Econ.CEA(
            strategies=[mono_therapy_strategy, combo_therapy_strategy],
            if_paired=False
        )
        # show the CE plane
        CEA.show_CE_plane(
            title='Cost-Effectiveness Analysis',
            x_label='Additional discounted utility',
            y_label='Additional discounted cost',
            show_names=True,
            show_clouds=True,
            show_legend=True,
            figure_size=6,
            transparency=0.3
        )
        # report the CE table
        CEA.build_CE_table(
            interval=Econ.Interval.CONFIDENCE,
            alpha=Settings.ALPHA,
            cost_digits=0,
            effect_digits=2,
            icer_digits=2,
        )

        # CBA
        NBA = Econ.CBA(
            strategies=[mono_therapy_strategy, combo_therapy_strategy],
            if_paired=False
        )
        # show the net monetary benefit figure
        NBA.graph_deltaNMB_lines(
            min_wtp=0,
            max_wtp=50000,
            title='Cost-Benefit Analysis',
            x_label='Willingness-to-pay for one additional QALY ($)',
            y_label='Incremental Net Monetary Benefit ($)',
            interval=Econ.Interval.CONFIDENCE,
            show_legend=True,
            figure_size=6
        )