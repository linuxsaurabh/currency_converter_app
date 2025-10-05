document.addEventListener('DOMContentLoaded', () => {
    const convertButton = document.getElementById('convert');
    const resultDiv = document.getElementById('result');

    convertButton.addEventListener('click', async () => {
        const amount = document.getElementById('amount').value;
        const from = document.getElementById('from').value;
        const to = document.getElementById('to').value;

        resultDiv.textContent = 'Converting...';

        try {
            const response = await fetch('/convert', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ amount, from, to })
            });
            const data = await response.json();

            if (!response.ok) throw new Error(data.error || JSON.stringify(data));

            resultDiv.innerHTML = `<strong>${data.amount} ${data.from}</strong> → <strong>${data.converted} ${data.to}</strong><br/>Rate: ${data.rate}`;
        } catch (err) {
            resultDiv.textContent = 'Error: ' + err.message;
        }
    });
});