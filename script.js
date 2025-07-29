// BMI Calculator Frontend Logic

document.addEventListener('DOMContentLoaded', function () {
    // BMI form
    const bmiForm = document.getElementById('bmiForm');
    const resultSection = document.getElementById('result');
    const loadingSection = document.getElementById('loading');
    const bmiValue = document.getElementById('bmiValue');
    const bmiCategory = document.getElementById('bmiCategory');

    if (bmiForm) {
        bmiForm.addEventListener('submit', async function (e) {
            e.preventDefault();
            // Get input values
            const weight = parseFloat(document.getElementById('weight').value);
            const height = parseFloat(document.getElementById('height').value);

            // Hide result, show loading
            resultSection.style.display = 'none';
            loadingSection.style.display = 'block';

            // Call backend API
            try {
                const response = await fetch('/calculate-bmi', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ weight, height })
                });
                const data = await response.json();
                loadingSection.style.display = 'none';
                if (data.success) {
                    bmiValue.textContent = data.bmi;
                    bmiCategory.textContent = data.category;
                    resultSection.style.display = 'block';
                } else {
                    alert(data.error || 'Error calculating BMI.');
                }
            } catch (err) {
                loadingSection.style.display = 'none';
                alert('Error connecting to server.');
            }
        });
    }

    // Mobile navigation
    const hamburger = document.querySelector('.hamburger');
    const navMenu = document.querySelector('.nav-menu');
    if (hamburger && navMenu) {
        hamburger.addEventListener('click', function () {
            hamburger.classList.toggle('active');
            navMenu.classList.toggle('active');
        });
        document.querySelectorAll('.nav-link').forEach(link => {
            link.addEventListener('click', () => {
                hamburger.classList.remove('active');
                navMenu.classList.remove('active');
            });
        });
    }
}); 