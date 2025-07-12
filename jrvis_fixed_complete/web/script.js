
async function startListening() {
  const response = await eel.listen_command()();
  document.getElementById("output").innerText = response;
}

async function sendCommand() {
  const input = document.getElementById("chatbox").value.trim();
  if (!input) return;
  const response = await eel.handle_command(input)();
  document.getElementById("output").innerText = response;
  document.getElementById("chatbox").value = "";
}
