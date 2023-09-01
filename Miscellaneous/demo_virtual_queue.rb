require 'signalwire/sdk'
require 'sinatra'

# TODO Configure your credentials
$project_id = 'PROJECT_ID_GOES_HERE'
$api_token = 'API_TOKEN_GOES_HERE'
$space_url = 'SPACE_GOES_HERE.signalwire.com'
$ngrok_url = "NGROK_URL_GOES_HERE"

$client = Signalwire::REST::Client.new($project_id, $api_token, signalwire_space_url: $space_url)

# Our makeshift queue
set :virtual_queue, []

# Our web server
set :port, 8080
set :bind, '0.0.0.0'

# Basic IVR to get a person to press 1.
post '/enqueue' do
  response = Signalwire::Sdk::VoiceResponse.new do |response|
    response.gather(action: '/process_enqueue', method: 'POST') do |gather|
      gather.say(message: 'Press 1 to be queued.')
    end
    response.say(message: 'We did not receive any input. Goodbye!')
  end
  response.to_s
end

# Handles the queueing process.
post '/process_enqueue' do
  response = Signalwire::Sdk::VoiceResponse.new

  if params['Digits'] == '1'
    settings.virtual_queue << params['From']  # Store caller's phone number in the queue
    response.say(message: 'You have been queued. Goodbye!')
    response.hangup
  end

  response.to_s
end

# Handles the agent's conference
post '/agent' do
  response = Signalwire::Sdk::VoiceResponse.new

  response.dial do |dial|
    dial.conference(
      'virtual_queue_conference',
      startConferenceOnEnter: true,
      endConferenceOnExit: true,
    )
  end
  response.to_s
end

# Handles the Callee and puts them in a conference and dials the agent afterwards.
post '/callee' do
  response = Signalwire::Sdk::VoiceResponse.new

  response.dial do |dial|
    dial.conference(
      'virtual_queue_conference',
      beep: false,
      startConferenceOnEnter: false,
      endConferenceOnExit: true,
      statusCallback: "#{$ngrok_url}/conference_status",
      statusCallbackEvent: 'join leave speaker',
      record: "record-from-start"
    )
  end
  call_agent
  response.to_s
end

# Handles the queue and dials back the callee
def process_virtual_queue
  settings.virtual_queue.each do |caller|
    call = $client.calls.create(
      from: '+1NUMBER_GOES_HERE', # TODO CHANGE THIS TO A NUMBER IN YOUR SPACE.
      to: caller,
      url: "#{$ngrok_url}/callee"
    )
    puts "Initiated call to #{caller}: Call SID #{call.sid}"

    settings.virtual_queue.delete(caller)  # Remove the caller from the queue
  end
end


# Agent Caller Handler
def call_agent
  agent_call = $client.calls.create(
    from: '+1NUMBER_GOES_HERE', # TODO CHANGE THIS TO A NUMBER IN YOUR SPACE.
    to: '+1NUMBER_GOES_HERE', # TODO CHANGE THIS TO A NUMBER. (Agent's phone number)
    url: "#{$ngrok_url}/agent"
  )
  puts "Initiated call to the agent: Call SID #{agent_call.sid}"
end

# Query the queue every 5 seconds to see if anyone is inside of it.
Thread.new do
  loop do
    process_virtual_queue
    sleep 5
  end
end

# Status Callback Event Handler
post '/conference_status' do
  # Handle conference status events as needed
  puts "Conference Status: #{params}"
end