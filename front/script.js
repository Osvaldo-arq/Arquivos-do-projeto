const API_URL = "http://localhost:8000/api/v1/invoice";

document.getElementById("uploadButton").addEventListener("click", uploadFile);

async function uploadFile() {
    const fileInput = document.getElementById("fileInput");
    const file = fileInput.files[0];

    if (!file) {
        alert("Selecione um arquivo primeiro!");
        return;
    }

    const loadingIndicator = document.getElementById("loading");
    const dataContainer = document.getElementById("dataContainer");

    loadingIndicator.classList.remove("hidden");
    dataContainer.classList.add("hidden");

    const formData = new FormData();
    formData.append("file", file);

    try {
        const response = await fetch(API_URL, {
            method: "POST",
            body: formData,
        });

        if (!response.ok) throw new Error("Erro no upload");

        await response.json();
        fetchProcessedData(file.name);
    } catch (error) {
        alert("Erro ao enviar o arquivo!");
    } finally {
        loadingIndicator.classList.add("hidden");
    }
}

async function fetchProcessedData(fileName) {
    try {
        const response = await fetch(`${API_URL}/${fileName}.json`);
        if (!response.ok) throw new Error("Erro ao buscar os dados");

        const data = await response.json();
        displayData(data);
    } catch (error) {
        alert("Erro ao buscar os dados processados!");
    }
}

function displayData(data) {
    const tableBody = document.querySelector("#dataTable tbody");
    tableBody.innerHTML = "";

    if (data && typeof data === 'object' && Object.keys(data).length > 0) {
        const rowValues = document.createElement("tr");
        let values = '';

        Object.values(data).forEach(value => {
            values += `<td>${value}</td>`;
        });

        rowValues.innerHTML = values;
        tableBody.appendChild(rowValues);
    } else {
        const row = document.createElement("tr");
        row.innerHTML = `<td colspan="2">Dados inválidos ou não encontrados.</td>`;
        tableBody.appendChild(row);
    }

    document.getElementById("dataContainer").classList.remove("hidden");
}