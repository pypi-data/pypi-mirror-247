--[[
  Function to move job from active state to wait.
  Input:
    KEYS[1] active key
    KEYS[2] wait key
    KEYS[3] stalled key
    KEYS[4] job lock key
    KEYS[5] paused key
    KEYS[6] meta key
    KEYS[7] limiter key
    KEYS[8] prioritized key
    KEYS[9] event key
    ARGV[1] job id
    ARGV[2] lock token
    ARGV[3] job id key
]]
local rcall = redis.call
-- Includes
--[[
  Function to push back job considering priority in front of same prioritized jobs.
]]
local function pushBackJobWithPriority(prioritizedKey, priority, jobId)
  -- in order to put it at front of same prioritized jobs
  -- we consider prioritized counter as 0
  local score = priority * 0x100000000
  rcall("ZADD", prioritizedKey, score, jobId)
end
--[[
  Function to check for the meta.paused key to decide if we are paused or not
  (since an empty list and !EXISTS are not really the same).
]]
local function getTargetQueueList(queueMetaKey, waitKey, pausedKey)
  if rcall("HEXISTS", queueMetaKey, "paused") ~= 1 then
    return waitKey, false
  else
    return pausedKey, true
  end
end
local jobId = ARGV[1]
local token = ARGV[2]
local lockKey = KEYS[4]
local lockToken = rcall("GET", lockKey)
local pttl = rcall("PTTL", KEYS[7])
if lockToken == token and pttl > 0 then
  local removed = rcall("LREM", KEYS[1], 1, jobId)
  if (removed > 0) then
    local target = getTargetQueueList(KEYS[6], KEYS[2], KEYS[5])
    rcall("SREM", KEYS[3], jobId)
    local priority = tonumber(rcall("HGET", ARGV[3], "priority")) or 0
    if priority > 0 then
      pushBackJobWithPriority(KEYS[8], priority, jobId)
    else
      rcall("RPUSH", target, jobId)
    end
    rcall("DEL", lockKey)
    -- Emit waiting event
    rcall("XADD", KEYS[9], "*", "event", "waiting", "jobId", jobId)
  end
end
return pttl
