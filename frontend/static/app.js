
let turnstileToken = "";

const verifyButton = document.getElementById("verify-button");
const verificationForm = document.getElementById("verification-form");
const message = document.getElementById("message");

function onTurnstileSuccess(token) {
    turnstileToken = token;
    verifyButton.disabled = false;
    message.textContent = "Verification completed. You can continue.";
    message.style.color = "green";
}

verificationForm.addEventListener("submit", async function (event) {
    event.preventDefault();

    if (!turnstileToken) {
        message.textContent = "Please complete verification.";
        return;
    }

    verifyButton.disabled = true;
    verifyButton.textContent = "Verifying...";

    try {
        const response = await fetch("/verify-human", {
            method: "POST",
            credentials: "same-origin",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                token: turnstileToken
            })
        });

        const result = await response.json();

        if (response.ok && result.success) {
            message.textContent = "Verification successful! Entering BookStore...";
            message.style.color = "green";

            window.location.replace("/store");
            return;
        }

        throw new Error(result.message || "Verification failed.");

    } catch (error) {
        message.textContent = error.message;
        message.style.color = "red";

        turnstileToken = "";

        if (window.turnstile) {
            window.turnstile.reset();
        }

        verifyButton.disabled = true;

    } finally {
        verifyButton.textContent = "Verify & Enter BookStore →";
    }
});
