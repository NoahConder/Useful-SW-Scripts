require 'signalwire/sdk'
require 'sinatra'

# TODO Configure your credentials
$project_id = 'PROJECT_ID_GOES_HERE'
$api_token = 'API_TOKEN_GOES_HERE'
$space_url = 'SPACE_GOES_HERE.signalwire.com'
$ngrok_url = "NGROK_URL_GOES_HERE"
$from_number = "FROM_NUMBER_FOR_THE_CALLS_GOES_HERE"
$coach_number = "THE_COACHES_SIP_ENDPOINT/NUMBER_GOES_HERE"
$agent_number = "THE_AGENTS_SIP_ENDPOINT/NUMBER_GOES_HERE"

$client = Signalwire::REST::Client.new($project_id, $api_token, signalwire_space_url: $space_url)

# Our web server
set :port, 8080
set :bind, '0.0.0.0'

# Handles the agent's conference
post '/agent' do
  response = Signalwire::Sdk::VoiceResponse.new

  response.dial do |dial|
    dial.conference(
      'coach_test',
      startConferenceOnEnter: true,
      endConferenceOnExit: true,
    )
  end
  call_coach
  response.to_s
end


# Handles the Callee
post '/callee' do
  response = Signalwire::Sdk::VoiceResponse.new

  response.dial do |dial|
    dial.conference(
      'coach_test',
      beep: false,
      startConferenceOnEnter: false,
      endConferenceOnExit: true,
      maxParticipants: "3",
      statusCallback: "#{$ngrok_url}/conference_status",
      statusCallbackEvent: 'join leave speaker',
      record: "record-from-start"
    )
  end
  call_agent
  response.to_s
end

post '/coach' do
  response = Signalwire::Sdk::VoiceResponse.new do |response|
    response.dial do |dial|
      dial.conference('coach_test', coach: $agent_call_sid)
    end
  end
  response.to_s
end

# Agent Caller Handler
def call_agent
  agent_call = $client.calls.create(
    from: $from_number,
    to: $agent_number,  # Agent's phone number
    url: "#{$ngrok_url}/agent"
  )
  $agent_call_sid = agent_call.sid
  puts "Initiated call to the agent: Call SID #{agent_call.sid}"
end

def call_coach
  call_coach = $client.calls.create(
    from: $from_number,
    to: $coach_number,  # Coach's phone number
    url: "#{$ngrok_url}/coach"
  )
  puts "Initiated call to the coach: Call SID #{call_coach.sid}"
end

# Status Callback Event Handler
post '/conference_status' do
  # Handle conference status events as needed
  puts "Conference Status: #{params}"
end