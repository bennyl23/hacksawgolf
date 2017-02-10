def score_to_par_converted(score_to_par):
    # translate the score_to_par integer field into a readable value for display
    if score_to_par is not None:
        if score_to_par == 0:
            return 'ev'
        elif score_to_par > 0:
            return '+' + str(score_to_par)

        return str(score_to_par)

    return 'N/A'


def status_converted(status, cut_point, made_the_cut):
    # return 'CUT' if status is None or '' and the cut point has been made and the player did not make the cut
    if (not status and cut_point and not made_the_cut):
        return 'CUT'

    return status

