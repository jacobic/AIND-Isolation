s script evaluates the performance of the custom_score evaluation
function against a baseline agent using alpha-beta search and iterative
deepening (ID) called `AB_Improved`. The three `AB_Custom` agents use
ID and alpha-beta search with the custom_score functions defined in
game_agent.py.

                        *************************                         
                                                     Playing Matches                              
                                                                             *************************                         

                                                                              Match #   Opponent    AB_Improved   AB_Custom   AB_Custom_2  AB_Custom_3 
                                                                                                      Won | Lost   Won | Lost   Won | Lost   Won | Lost 
                                                                                                          1       Random      90  |  10    92  |   8    94  |   6    92  |   8  
                                                                                                              2       MM_Open     63  |  37    73  |  27    64  |  36    69  |  31  
                                                                                                                  3      MM_Center    90  |  10    85  |  15    86  |  14    85  |  15  
                                                                                                                      4     MM_Improved   66  |  34    69  |  31    62  |  38    63  |  37  
                                                                                                                          5       AB_Open     50  |  50    51  |  49    47  |  53    49  |  51  
                                                                                                                              6      AB_Center    61  |  39    58  |  42    53  |  47    58  |  42  
                                                                                                                                  7     AB_Improved   43  |  57    42  |  58    50  |  50    47  |  53  
                                                                                                                                  --------------------------------------------------------------------------
                                                                                                                                             Win Rate:      66.1%        67.1%        65.1%        66.1%    

                                                                                                                                             There were 5.0 timeouts during the tournament -- make sure your agent handles search timeout correctly, and consider increasing the timeout margin for your agent.

    # delta player distances to center, penalize peripheral positions, adjust move 
        # heuristics etc. got me to 77%  in one run. these are purely context free 
            # heuristic. if we add look ahead moves etc we can improve it further.
                # @barni if you look ahead in moves for heuristics that's equivalent of doing 
                    #a recursive search inside a recursive. imo unnecessary to finish this project, 
                        #but to each his own. a more efficient way is running some simple policy mapping similar to the case in q learning, by running tons of games, run some statistics, and derive weights to to each cell as a function of the number of move played.
                            # Han Lee 
                                # @barni aka supervised learning a policy network, put that down as your 
                                    # heuristics function. effectively turning a simple search into reinforcement 
                                        # learning search w/o policy gradients
                                            
                                                #With knights we simply encourage them to go to the center. Standing on the 
                                                    #edge is a bad idea. Standing in the corner is a terrible idea. Probably 
                                                        #it was Tartakover who said that "one piece stands badly, the whole game 
                                                            #stands badly". And knights move slowly.
                                                                
                                                                    #Most evaluations terms are a linear combination of independent features and associated weights
                                                                        
