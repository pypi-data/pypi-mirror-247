from time import sleep
from random import randint

def assert_func(if_method, variable1_assertion_required, variable2_assertion_required):
    state = "ALPHA"
    acceptable_if = ["equal", "greater", "less_than"]

    if if_method in acceptable_if:
        if if_method == "equal":
            if variable1_assertion_required == variable2_assertion_required:
                random_sleep = randint(0, 1)
                sleep(random_sleep)
                print(f"""
                
                ----- TEST SESSION STARTS -----
                Test 1:
                    {variable1_assertion_required} == {variable2_assertion_required}
                    Asserted
                ////// {state} VERSION, ONLY ONE TEST ALLOWED AND TWO VARIABLES AT A TIME ///////

                ----- TEST RAN IN {random_sleep}s ------
                
                """)
            else:
                random_sleep = randint(0, 1)
                sleep(random_sleep)
                print(f"""
                
                ----- TEST SESSION STARTS -----
                Test 1:
                    {variable1_assertion_required} == {variable2_assertion_required}
                    Failed
                ////// {state} VERSION, ONLY ONE TEST ALLOWED AND TWO VARIABLES AT A TIME ///////

                ----- TEST RAN IN {random_sleep}s ------
                
                """)
        elif if_method == "greater":
            if variable1_assertion_required > variable2_assertion_required:
                random_sleep = randint(0, 1)
                sleep(random_sleep)
                print(f"""
                
                ----- TEST SESSION STARTS -----
                Test 1:
                    {variable1_assertion_required} > {variable2_assertion_required}
                    Asserted
                    
                    if result isnt what you expected, change the variable position or
                    the if_method to {acceptable_if[2]}

                ////// {state} VERSION, ONLY ONE TEST ALLOWED AND TWO VARIABLES AT A TIME ///////

                ----- TEST RAN IN {random_sleep}s ------
                
                """)
            else:
                random_sleep = randint(0, 1)
                sleep(random_sleep)
                print(f"""
                
                ----- TEST SESSION STARTS -----
                Test 1:
                    {variable1_assertion_required} > {variable2_assertion_required}
                    Failed
                    
                    if result isnt what you expected, change the variable position or
                    the if_method to {acceptable_if[2]}

                ////// {state} VERSION, ONLY ONE TEST ALLOWED AND TWO VARIABLES AT A TIME ///////

                ----- TEST RAN IN {random_sleep}s ------
                
                """)
        elif if_method == "less_than":
            if variable1_assertion_required < variable2_assertion_required:
                random_sleep = randint(0, 1)
                sleep(random_sleep)
                print(f"""
                
                ----- TEST SESSION STARTS -----
                Test 1:
                    {variable1_assertion_required} < {variable2_assertion_required}
                    Asserted
                    
                    if result isnt what you expected, change the variable position or
                    the if_method to {acceptable_if[1]}

                ////// {state} VERSION, ONLY ONE TEST ALLOWED AND TWO VARIABLES AT A TIME ///////

                ----- TEST RAN IN {random_sleep}s ------
                
                """)
            else:
                random_sleep = randint(0, 1)
                sleep(random_sleep)
                print(f"""
                
                ----- TEST SESSION STARTS -----
                Test 1:
                    {variable1_assertion_required} < {variable2_assertion_required}
                    Failed
                    
                    if result isnt what you expected, change the variable position or
                    the if_method to {acceptable_if[1]}

                ////// {state} VERSION, ONLY ONE TEST ALLOWED AND TWO VARIABLES AT A TIME ///////

                ----- TEST RAN IN {random_sleep}s ------
                
                """) 
    else:
        print(f"""
        
        "{if_method}" is not an acceptable if_method that
        the function accepts.

        Please use:
        ----------------------------------------------------------------
        ---- equal
        ---- greater
        ---- less_than
        ----------------------------------------------------------------
        """) 