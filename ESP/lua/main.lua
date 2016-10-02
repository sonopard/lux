ws2812.init()

-- set up a timer
-- timer function: begin displaying a simple pattern

function start_udp_server()
  s = net.createServer(net.UDP)
  -- can we buffer this and use a proper header?
  -- what about the ip display stuff the ccc hannover guys did?
  s:on("receive",function(s,c) 
    ws2812.write(c)
    -- if timer
    -- reset the timer
    -- stop the pattern
  end)
  s:listen(2342)
end

start_udp_server()

