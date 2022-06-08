# Import the MachUpX module
import machupX as MX

# Input the json module to make displaying dictionaries more friendly
import json


if __name__=="__main__":

    # Define the aircraft
    aircraft_input = {
        "CG" : [0,0,0],
        "weight" : 40.0,
        "controls" : {
            "aileron" : {
                "is_symmetric" : False
            },
            "elevator" : {
                "is_symmetric" : True
            },
            "rudder" : {
                "is_symmetric" : False
            }
        },
        "airfoils" : "airfoils.json",
        "wings" : {
            "main_wing" : {
                "ID" : 1,
                "side" : "both",
                "is_main" : True,
                "semispan" : 4.0,
                "dihedral" : 5.0,
                "chord" : [[0.0, 1.5],
                           [1.0, 1.0]],
                "airfoil" : "NACA2410",
                "control_surface" : {
                    "chord_fraction" : 0.25,
                    "root_span" : 0.5,
                    "tip_span" : 1.0,
                    "control_mixing" : {
                        "aileron" : 1.0
                    }
                },
                "grid" : {
                    "N" : 40
                }
            },
            "h_stab" : {
                "ID" : 2,
                "side" : "both",
                "is_main" : False,
                "connect_to" : {
                    "ID" : 1,
                    "location" : "root",
                    "dx" : -4.0,
                    "dz" : -0.5
                },
                "semispan" : 2.0,
                "chord" : [[0.0, 1.0],
                           [1.0, 0.75]],
                "sweep" : 10.0,
                "airfoil" : "NACA0010",
                "control_surface" : {
                    "chord_fraction" : 0.5,
                    "control_mixing" : {
                        "elevator" : 1.0
                    }
                },
                "grid" : {
                    "N" : 20
                }
            },
            "v_stab" : {
                "ID" : 3,
                "side" : "left",
                "is_main" : False,
                "connect_to" : {
                    "ID" : 1,
                    "location" : "root",
                    "dx" : -4.0,
                    "dz" : -0.51
                },
                "semispan" : 1.0,
                "dihedral" : 90.0,
                "sweep" : 30.0,
                "chord" : [[0.0, 1.0],
                           [1.0, 0.75]],
                "airfoil" : "NACA0010",
                "control_surface" : {
                    "chord_fraction" : 0.5,
                    "control_mixing" : {
                        "rudder" : 1.0
                    }
                },
                "grid" : {
                    "N" : 20
                }
            }
        }
    }


    # Initialize Scene object
    my_scene = MX.Scene()

    # Add aircraft
    state = {
        "velocity" : 100.0,
        "alpha" : 2.0
    }
    my_scene.add_aircraft("goates_flier", aircraft_input, state=state)

    # Check out the airplane
    my_scene.display_wireframe(show_vortices=False)

    # See what forces are acting on the airplane
    FM_results = my_scene.solve_forces(dimensional=True, non_dimensional=False)
    print(json.dumps(FM_results["goates_flier"]["total"], indent=4))

    # Now let's get the airplane to its trim state in pitch
    trim_state = my_scene.pitch_trim(set_trim_state=True, verbose=True)
    print(json.dumps(trim_state["goates_flier"], indent=4))

    # See what forces are acting on the airplane
    FM_results = my_scene.solve_forces(dimensional=True, non_dimensional=False)
    print(json.dumps(FM_results["goates_flier"]["total"], indent=4))

    # Now that we're trimmed, let's see what our aerodynamic derivatives are
    derivs = my_scene.derivatives()
    print(json.dumps(derivs["goates_flier"], indent=4))