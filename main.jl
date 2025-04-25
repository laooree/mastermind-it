#= This code will try to guess the sequence provided by the user. It will do so
by using information theory, and trying guesses that maximized the expected
information value, until the correct solution is found.

The game is structured so that the sequence is four-digitis long, with digits
from 0 to 9. 10'000 combinations are therefore possible.

In future versions I'll add arbitrary sequence length.
=#



function get_hints(guess,solution)
  # Return the hints for the given guess and solution.
  # hints[1]: how many in correct place
  # hints[2]: how many in wrong place
  
  hints = [0,0] # initialize hints

  # Multiple runs
  # First run: count hints[1]. The vector remaining stores the indices where no
  # match is found, which are then parsed when counting hints[2].
  remaining = [];
  for i in 1:length(solution) # cycle through all elements
    if guess[i] == solution[i]
      # correct digit in the correct place found
      hints[1] += 1
    else
      append!(remaining,i)
    end
  end

  # Second run: count hints[2], among the remaining elements.
  remaining_solution = remaining
  for i in remaining
    for j in remaining_solution
      if i != j && guess[i] == solution[j]
        hints[2] += 1
        # remove matching index and break, so that it is not counted multiple
        # times
        filter!(x->x≠j,remaining_solution)
        break
      end
    end
  end

  return hints
  
end



function string_to_array(s)
  # convert the string s, which represent an integer number, into an array with
  # its digits as elements.

  a = zeros(Int,length(s));

  for k in 1:length(s)
    a[k] = parse(Int,s[k]);
  end

  return a

end



################
##### Main #####
################

function main()

  println("Please, insert the secret sequence:")
  solution = string_to_array(readline())
  N = length(solution)

  possibilities = zeros(Int, 10^N, N)
  possible_hints = zeros(Int, (N+1)^2, 2)

  for k = 1:(10^N)-1
    k_string = string(k)
    for h = 1:length(k_string)
      possibilities[k, end-h+1] = parse(Int, k_string[end-h+1])
    end
  end

  for k = 1:length(possible_hints[:, 1])
    possible_hints[k, 2] = (k-1) % (N+1)
    possible_hints[k, 1] = floor((k-1) / (N+1))
  end

  not_solved = true
  while not_solved
    Np = size(possibilities, 1)
    expected_information = zeros(Np)

    for i = 1:Np
      for j = 1:size(possible_hints, 1)
        p = 0.0
        for h = 1:Np
          if possible_hints[j, :] == get_hints(possibilities[h, :], possibilities[i, :])
            p += 1.0
          end
        end
        if p > 0
          expected_information[i] += -p/Np * log2(p/Np)
        end
      end
    end

    guess = possibilities[rand(findall(x -> x == maximum(expected_information), expected_information)), :]

    hints = get_hints(guess, solution)
    if hints == [N, 0]
      println("Solution found:")
      println(guess)
      not_solved = false
    else
      println()
      println("I chose the following guess:")
      println(guess)
      println("And I got the following hints:")
      println(hints)
    end

    new_possibilities = Int[]
    for k = 1:Np
      if get_hints(guess, possibilities[k, :]) == hints
        push!(new_possibilities, k)
      end
    end

    possibilities = possibilities[new_possibilities, :]
  end
end


main()
