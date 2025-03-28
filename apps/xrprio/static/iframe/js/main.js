import { SceneManager } from './scene_manager.js';

const canvas = document.getElementById("threejsCanvas");
const sceneManager = new SceneManager(canvas);

bindEventListeners();
render();

function bindEventListeners() {
	window.addEventListener('resize', resizeCanvas);
	resizeCanvas();
}

function resizeCanvas() {
	canvas.style.width = '100%';
	canvas.style.height = '500px';

	canvas.width = canvas.offsetWidth;
	canvas.height = canvas.offsetHeight;

	sceneManager.onWindowResize();
}

function render() {
	requestAnimationFrame(render);
	sceneManager.update();
}
