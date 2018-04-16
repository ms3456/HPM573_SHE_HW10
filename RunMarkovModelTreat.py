import ParameterClasses as P
import MarkovModel as MarkovCls
import SupportMarkovModel as SupportMarkov
import scr.SamplePathClasses as PathCls
import scr.FigureSupport as Figs

# create and simulate cohort
cohort_none = MarkovCls.Cohort(
    id=1,
    therapy=P.Therapies.NONE)

simOutputs_none = cohort_none.simulate()

# graph survival curve
PathCls.graph_sample_path(
    sample_path=simOutputs_none.get_survival_curve(),
    title='Survival curve',
    x_label='Simulation time step',
    y_label='Number of alive patients'
    )

# graph histogram of survival times
Figs.graph_histogram(
    data=simOutputs_none.get_survival_times(),
    title='Survival times of patients with Stroke',
    x_label='Survival time (years)',
    y_label='Counts',
    bin_width=1
)

# graph histogram of number of strokes
Figs.graph_histogram(
    data=simOutputs_none.get_if_developed_stroke(),
    title='Number of Strokes per Patient',
    x_label='Strokes',
    y_label='Counts',
    bin_width=1
)

# print outcomes (means and CIs)
SupportMarkov.print_outcomes(simOutputs_none, 'No Treatment:')

# create and simulate cohort
cohort_anticoag = MarkovCls.Cohort(
    id=1,
    therapy=P.Therapies.ANTICOAG)

simOutputs_anticoag = cohort_anticoag.simulate()

# graph survival curve
PathCls.graph_sample_path(
    sample_path=simOutputs_anticoag.get_survival_curve(),
    title='Survival curve',
    x_label='Simulation time step',
    y_label='Number of alive patients'
    )

# graph histogram of survival times
Figs.graph_histogram(
    data=simOutputs_anticoag.get_survival_times(),
    title='Survival times of patients with Stroke',
    x_label='Survival time (years)',
    y_label='Counts',
    bin_width=1
)

# graph histogram of number of strokes
Figs.graph_histogram(
    data=simOutputs_anticoag.get_if_developed_stroke(),
    title='Number of Strokes per Patient',
    x_label='Strokes',
    y_label='Counts',
    bin_width=1
)

# print outcomes (means and CIs)
SupportMarkov.print_outcomes(simOutputs_anticoag, 'Treatment:')


# print comparative outcomes
SupportMarkov.print_comparative_outcomes(simOutputs_mono=simOutputs_none,
                                         simOutputs_combo=simOutputs_anticoag)

# report the CEA results
SupportMarkov.report_CEA_CBA(simOutputs_mono=simOutputs_none, simOutputs_combo=simOutputs_anticoag)
