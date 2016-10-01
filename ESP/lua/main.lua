ws2812.init()

value = true
function start_testblink()
  tmr.alarm(0, 500, 1, function ()
    if (value) then
      ws2812.write(string.char(255, 0, 0, 255, 0, 0))	    
    else
      ws2812.write(string.char(0, 0, 255, 0, 0, 255))	    
    end
    value = not value
  end )
end

function start_udp_server()
  s = net.createServer(net.UDP)
  s:on("receive",function(s,c) 
    ws2812.write(c)
  end)
  s:listen(2342)
end

start_udp_server()

