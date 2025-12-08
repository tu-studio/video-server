local socket = require("socket")

local udp = assert(socket.udp())
udp:setsockname("*", 5000)
udp:settimeout(0)

local function handle(msg)
    -- example: receive "pause", "resume", "stop"
    if msg == "pause" then
        mp.set_property("pause", true)
    elseif msg == "resume" then
        mp.set_property("pause", false)
    elseif msg:match("^load ") then
        local path = msg:sub(6)
        mp.commandv("loadfile", path, "replace")
    elseif msg == "stop" then
        mp.commandv("stop")
    end
end

mp.add_periodic_timer(0.01, function()
    local data = udp:receive()
    if data then handle(data) end
end)

