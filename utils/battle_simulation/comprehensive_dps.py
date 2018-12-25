from simple_cycle_dps import _get_move_dps, _get_move_eps, simple_cycle_dps


# https://pokemongo.gamepress.gg/how-calculate-comprehensive-dps
def comprehensive_dps(pokemon_1, quick_move_1, charge_move_1,
                      pokemon_2, quick_move_2, charge_move_2, type_data):
    # Pull fast and charge move DPS from simple calculation
    fdps = _get_move_dps(pokemon_1, quick_move_1, pokemon_2, type_data)
    cdps = _get_move_dps(pokemon_1, charge_move_1, pokemon_2, type_data)

    # Pull fast and charge move EPS from simple calculation
    feps = _get_move_eps(quick_move_1)
    ceps = _get_move_eps(charge_move_1)

    # we want to implement the following formula:
    # DPS = DPS_o + EE * ENERGY_CORRECTION
    # where DPS_o is the simple DPS
    # EE is the "energy efficiency" i.e. extra damage per energy
    # ENERGY_CORRECTION corrective term for energy gained through taking dmg

    # constants for our formula

    # estimate enemy damage using simple only, so we don't solve linear system
    enemy_dps_estimate = simple_cycle_dps(pokemon_2, quick_move_2, charge_move_2, pokemon_1, type_data)
    # health of the subject pokemon
    hp = pokemon_1.remaining_hp
    # assume we use all of our gained energy perfectly
    # TODO: we can try to estimate this value instead using E[x]
    remaining_energy = 0

    # DPS_o
    simple_dps = simple_cycle_dps(pokemon_1, quick_move_1, charge_move_1, pokemon_2, type_data)

    # EE
    energy_efficiency = _calculate_energy_efficiency(fdps, feps, cdps, ceps)

    # ENERGY_CORRECTION
    e_correction = _calculate_energy_correction(remaining_energy, enemy_dps_estimate, hp)

    comp_dps = simple_dps + energy_efficiency * e_correction

    return comp_dps


# estimate x and y using a good guess for E[x] and E[y]
def _get_optimal_unknowns(ce, fe, num_bar, e_fdmg, e_cdmg, e_fdur, e_cdur):
    if num_bar == 1:
        lam = 3
    elif num_bar == 2:
        lam = 1.5
    else:
        lam = 1

    average_energy_left = 0.5 * ce + 0.5 * fe + 0.5 * ((1.0 * lam * e_fdmg + e_cdmg) / (lam + 1))
    average_enemy_dps = (1.0 * lam * e_fdmg + e_cdmg) / (1.0 * lam * (e_fdur + 2) + e_cdur + 2)

    return average_energy_left, average_enemy_dps


def _calculate_energy_correction(energy_left, enemy_dps, hp):
    return 1.0 * (0.5 - energy_left / hp) * enemy_dps


def _calculate_energy_efficiency(fdps, feps, cdps, ceps):
    return 1.0 * (cdps - fdps) / (ceps + feps)
