-- a simple multiuser telnet server
-- author thejeremail

telnet_srv_clients = {}
telnet_srv = net.createServer(net.TCP, 180)
telnet_srv_fifo = {}
telnet_srv_fifo_drained = true

function telnet_srv_node_output(str)
	table.insert(telnet_srv_fifo, str)
end

function telnet_srv_distribute_output()
	if #telnet_srv_fifo > 0 then
		local msg = table.remove(telnet_srv_fifo, 1)
        for a,client in ipairs(telnet_srv_clients) do
		    client:send(msg)
			client:send("> ")
	    end
		tmr.alarm(6,70,tmr.ALARM_SINGLE,telnet_srv_distribute_output)
	else
	    fifo_drained = true
	end
end

function telnet_srv_s_output(str)
    table.insert(telnet_srv_fifo, str.."\n> ")
    uart.write(0,"\n> ")
	telnet_srv_distribute_output()
end
node.output(telnet_srv_s_output, 1)

telnet_srv:listen(23, function(socket)

    socket:on("receive", function(c, l)
        node.input(l)           -- works like pcall(loadstring(l)) but support multiple separate line
    end)
    socket:on("disconnection", function(c)
        local self = 31
		for a,client in ipairs(telnet_srv_clients) do
			if client == c then
				self = a
			end
		end
		table.remove(telnet_srv_clients,self)
    end)
	table.insert(telnet_srv_clients,socket)
	local ip = socket:getpeer()
    print("New Connection from "..ip..".")
end)

