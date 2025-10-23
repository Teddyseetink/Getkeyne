const textbox = document.getElementById("textbox")
const clicktocopy = document.getElementById("aaaa")
const prams = new URL(window.location.href).searchParams;
let abc = "/index.html"
if (prams.get("key")) {
    textbox.innerHTML = prams.get("key")
} else if (prams.get("redirect")) {
    abc = "https://link4m.com/"+ prams.get("redirect")
}
async function copyToClipboard() {
  try {
    await navigator.clipboard.writeText(prams.get("key"));
    clicktocopy.innerHTML = "Copied Key"
    clicktocopy.className = "bcontinuee2"
    setTimeout(function() {
        clicktocopy.innerHTML = "Click to copy"
        clicktocopy.className = "bcontinuee"
    }, 2000);
  } catch (err) {
  }
}

function to() {
    window.location.href = abc
}