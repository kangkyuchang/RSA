let selectedE = 65537;
function openTab(evt, tabName) {
    const tabContents = document.getElementsByClassName("tab-content");
    for (let content of tabContents) {
        content.classList.remove("active");
    }

    const tabLinks = document.getElementsByClassName("tab-link");
    for (let link of tabLinks) {
        link.classList.remove("active");
    }

    document.getElementById(tabName).classList.add("active");
    evt.currentTarget.classList.add("active");
}

async function generateAutoKey(button) {
    button.disabled = true;
    const response = await fetch('/api/generate-key', {
        method: "get"
    });

    const data = await response.json();
    const publicKeyArea = document.getElementById("auto-gen-public");
    publicKeyArea.innerText = data.publicKey;
    const privateKeyArea = document.getElementById("auto-gen-private");
    privateKeyArea.innerText = data.privateKey;
    const nArea = document.getElementById("auto-gen-n");
    nArea.innerText = data.N;

    button.disabled = false;
}

async function generateManualKey(button) {
    const pInput = document.getElementById("prime-p-input").value;
    const qInput = document.getElementById("prime-q-input").value;
    if(!pInput || !qInput)
        return;
    button.disabled = true;
    const playlod = {
        p: pInput,
        q: qInput,
        e: selectedE
    }
    const response = await fetch('/api/generate-key', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(playlod)
    });

    const data = await response.json();
    if(data.status == -1) {
        alert("p,q 중 소수가 아닌 수가 있어 키를 생성하지 못하였습니다.");
        button.disabled = false;
        return;
    }
    else if(data.status == 0) {
        alert("선택한 암호화 지수(e)가 유효하지 않아 랜덤으로 선택되었습니다.");
    }
    const publicKeyArea = document.getElementById("manual-gen-public");
    publicKeyArea.innerText = data.publicKey;
    const privateKeyArea = document.getElementById("manual-gen-private");
    privateKeyArea.innerText = data.privateKey;
    const nArea = document.getElementById("manual-gen-n");
    nArea.innerText = data.N;

    button.disabled = false;
}

async function checkPrime(type) {
    const inputElement = document.getElementById(`prime-${type}-input`);
    const errorElement = document.getElementById(`prime-${type}-error`);
    if(inputElement.value == "")
        return;
    const playlod = {
        p: inputElement.value
    }
    const response = await fetch('/api/check-prime', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(playlod)
    });

    const data = await response.json();
    if(data.isPrime) {
        inputElement.classList.remove('invalid');
        errorElement.style.display = 'none';
        const anotherInputElement = type == "p" ? document.getElementById("prime-q-input") : document.getElementById("prime-p-input");
        if(anotherInputElement.value == "")
            return;
        getPHI(inputElement.value, anotherInputElement.value);
    }
    else {
        inputElement.classList.add('invalid');
        errorElement.style.display = 'block';
    }
}

async function getPHI(num1, num2) {
    const playlod = {
        p: num1,
        q: num2
    }

    const response = await fetch('/api/get-phi', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(playlod)
    });

    const data = await response.json();
    const phiElement = document.getElementById("phi-value");
    phiElement.innerText = "";
    if(data.isValid) {
        phiElement.innerText = data.phi;
    }
}

function selectE(element) {
    selectedE = element.innerText;
    
    const chips = document.querySelectorAll(".chip");
    chips.forEach(chip => chip.classList.remove("active"));
    
    element.classList.add("active");
    
    hideCustomE();
}

function toggleCustomE(button) {
    const phiElement = document.getElementById("phi-value");
    if(phiElement.innerText == "" || phiElement.innerText > 65337) {
        alert("직접 입력은 오일러 피 함수가 65537 이하만 가능합니다.");
        return;
    }
    const wrapper = document.getElementById('custom-e-wrapper');
    
    const chips = document.querySelectorAll('.chip');
    chips.forEach(chip => chip.classList.remove('active'));
    button.classList.add('active');
    
    wrapper.classList.add('show');
    document.getElementById('custom-e-input').focus();
}

function hideCustomE() {
    document.getElementById("custom-e-wrapper").classList.remove("show");
}

async function isValidE() {
    const eInput = document.getElementById('custom-e-input');
    const statusMsg = document.getElementById('status-e');
    const eValue = eInput.value;
    const phiElement = document.getElementById("phi-value");
    if(phiElement.innerText == "" || !eValue)
        return;
    const playlod = {
        e: eValue,
        phi: parseInt(phiElement.innerText)
    }

    const response = await fetch('/api/check-exponent', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(playlod)
    });

    const data = await response.json();
    if(data.isValid) {
        statusMsg.textContent = "✅ 사용 가능한 유효한 e 값입니다.";
        statusMsg.className = "status-msg success";
        eInput.classList.remove('invalid');
        eInput.classList.add('valid');
        selectedE = parseInt(eValue);
    }
    else {
        statusMsg.textContent = "❌ φ(n)과 서로소가 아닙니다. 다른 값을 입력하세요.";
        statusMsg.className = "status-msg error";
        eInput.classList.remove('valid');
        eInput.classList.add('invalid');
    }
}

async function encryptText() {
    const plainTextArea = document.getElementById("plain-text-area").value;

    const publicKeyValue = document.getElementById("direct-public-key").value;
    const nValue = document.getElementById("direct-n").value;

    if(!plainTextArea || !publicKeyValue || !nValue)
        return;

    const playlod = {
        publicKey: publicKeyValue,
        N: nValue,
        text: plainTextArea
    }

    const response = await fetch('/api/encrypt', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(playlod)
    });

    const data = await response.json();
    const chiperTextArea = document.getElementById("cipher-text-area");
    chiperTextArea.value = data.cipherText;
}

async function decryptText() {
    const chiperTextArea = document.getElementById("cipher-text-area").value;

    const privateKeyValue = document.getElementById("direct-private-key").value;
    const nValue = document.getElementById("direct-n").value;

    if(!chiperTextArea || !privateKeyValue || !nValue)
        return;

    const playlod = {
        privateKey: privateKeyValue,
        N: nValue,
        text: chiperTextArea
    }

    const response = await fetch('/api/decrypt', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(playlod)
    });

    const data = await response.json();
    const plainTextArea = document.getElementById("plain-text-area");
    plainTextArea.value = data.plainText;
}

function downloadKey(data, fileName) {
    const jsonString = JSON.stringify(data, null, 2);

    const blob = new Blob([jsonString], { type: "application/json" });

    const url = URL.createObjectURL(blob);

    const link = document.createElement("a");
    link.href = url;
    link.download = fileName;
    
    document.body.appendChild(link);
    link.click();

    document.body.removeChild(link);
    URL.revokeObjectURL(url);
}