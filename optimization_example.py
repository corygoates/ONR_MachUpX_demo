import json
import machupX as MX
import scipy.optimize as sopt


def get_goates_flier_trim_drag(V):
    # Calculates the trim drag at the given cruise speed

    print()
    print("Velocity", V)

    # Initialize Scene object
    my_scene = MX.Scene()

    # Add aircraft
    state = {
        "velocity" : V,
        "alpha" : 2.0
    }
    my_scene.add_aircraft("goates_flier", "goates_flier.json", state=state)

    # Trim
    trim_result = my_scene.pitch_trim(set_trim_state=True)
    print(json.dumps(trim_result, indent=4))

    # Get drag
    forces = my_scene.solve_forces(nondimensional=False)

    D = forces["goates_flier"]["total"]["FD"]
    print("Drag Force", D)
    return D


if __name__=="__main__":

    # Define objective function
    def f(V):
        return get_goates_flier_trim_drag(V)

    # Optimize
    result = sopt.minimize_scalar(f, bounds=[75.0, 250.0], method="Bounded")
    print()
    print("A cruise speed of {0} ft/s will give a minimum drag of {1} lbf.".format(result.x, result.fun))