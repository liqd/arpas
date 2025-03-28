import * as THREE from 'https://cdnjs.cloudflare.com/ajax/libs/three.js/110/three.module.js';
import { loadGLTFModel, setModelPosition, setModelRotation, setModelScale } from './gltf_model_loader.js';

export class SceneManager {
    /**
     * Constructor for the SceneManager class.
     * Initializes the canvas, dimensions, scene, renderer, camera, and subjects.
     * @param {HTMLCanvasElement} canvas - The HTML canvas element for rendering the scene.
     */
    constructor(canvas) {
        this.canvas = canvas;
        console.log(this.canvas); // DEBUG
        this.clock = new THREE.Clock();

        this.canvasDimensions = {
            width: canvas.width,
            height: canvas.height,
        };

        this.scene = this.buildScene();
        this.renderer = this.buildRenderer(this.canvasDimensions);
        this.camera = this.buildCamera(this.canvasDimensions);
        this.sceneSubjects = this.createSceneSubjects(this.scene);

        this.setupCameraFeed();

        this.directionalInput = 'none';
        window.addEventListener('message', (event) => {
            const { action, direction } = event.data;
            if (action === 'directionalInput') {
                this.directionalInput = direction;
            }
        });

        // Load a GLTF model
        loadGLTFModel(this.scene, "/static/iframe/gltf_models/bench/scene.gltf",
            { x: 0, y: 0, z: 0 }, { x: 0, y: -90, z: 0}, { x: .2, y: .2, z: .2 })
            .then((model) => {
                this.loadedModel = model;
                console.log('Model loaded successfully:', model);
            })
            .catch((error) => {
                console.error('Error loading the model:', error);
            });

        // Detect plane and place model
        // this.detectPlane(this.renderer)
        //     .then((position) => {
        //         console.log('Detected plane at:', position);
        //         setModelPosition(loadedModel, position);
        //     })
        //     .catch((error) => {
        //         console.error('Error placing the model:', error);
        //     });
    }

    update() {
        const elapsedTime = this.clock.getElapsedTime();
        // Rotate each subject in the scene
        this.sceneSubjects.forEach((subject) => {
            subject.rotation.x += 0.01; // Adjust rotation speed as needed
            subject.rotation.y += 0.01;
        });
        // subject.update(elapsedTime, this.directionalInput));
        this.renderer.render(this.scene, this.camera);
        this.directionalInput = 'none';
    }

    /**
     * Builds the Three.js scene object.
     * @returns {THREE.Scene} - The initialized scene object.
     */
    buildScene() {
        const scene = new THREE.Scene();
        scene.background = new THREE.Color("#000"); // Set background color to black
        return scene;
    }

    /**
     * Creates and configures the WebGL renderer.
     * Binds the renderer to the specified canvas and sets pixel ratio and size.
     * @param {Object} canvasDimensions - Dimensions of the canvas (width, height).
     * @returns {THREE.WebGLRenderer} - The configured renderer.
     */
    buildRenderer({ width, height }) {
        const renderer = new THREE.WebGLRenderer({ canvas: this.canvas, antialias: true, alpha: true });
        const DPR = window.devicePixelRatio || 1;
        renderer.setPixelRatio(DPR);
        renderer.setSize(width, height);
        renderer.outputColorSpace = THREE.SRGBColorSpace;
        return renderer;
    }

    /**
     * Creates and configures a perspective camera.
     * Sets the aspect ratio, field of view, and clipping planes.
     * Positions the camera to view the scene properly.
     * @param {Object} canvasDimensions - Dimensions of the canvas (width, height).
     * @returns {THREE.PerspectiveCamera} - The configured camera.
     */
    buildCamera({ width, height }) {
        const aspectRatio = width / height;
        const fieldOfView = 60;
        const nearPlane = 0.1;
        const farPlane = 1000;
        const camera = new THREE.PerspectiveCamera(fieldOfView, aspectRatio, nearPlane, farPlane);
        camera.position.set(0, 0, 10);
        return camera;
    }

    /**
     * Sets up the device's camera feed as the scene background.
     * Requests access to the user's camera, plays the video, and creates a video texture.
     * Handles any errors in accessing the camera.
     */
    async setupCameraFeed() {
        try {
            // Request access to the user's camera
            const stream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: 'environment' } });

            // Create a video element to hold the camera stream
            const video = document.createElement('video');
            video.srcObject = stream;
            video.play();

            // Create a video texture from the camera feed
            const videoTexture = new THREE.VideoTexture(video);
            videoTexture.colorSpace = THREE.SRGBColorSpace;

            // Set the video as the scene background
            this.scene.background = videoTexture;

        } catch (error) {
            console.error('Error accessing the camera:', error);
        }
    }

    /**
     * Detects a plane in the AR environment and retrieves its position.
     * Uses WebXR hit testing to find a valid location on a detected plane.
     * @param {THREE.WebGLRenderer} renderer - The WebGL renderer with WebXR enabled.
     * @returns {Promise<Object>} - A promise that resolves to an object containing x, y, and z coordinates.
     */
    async detectPlane(renderer) {
        try {
            // Request AR session with hit test feature
            const session = await navigator.xr.requestSession('immersive-ar', {
                requiredFeatures: ['plane-detection', 'hit-test']
            });

            const referenceSpace = await session.requestReferenceSpace('local');
            const viewerSpace = await session.requestReferenceSpace('viewer');
            const hitTestSource = await session.requestHitTestSource({ space: viewerSpace });

            return new Promise((resolve, reject) => {
                const renderLoop = () => {
                    const frame = renderer.xr.getFrame();

                    if (hitTestSource) {
                        const hitTestResults = frame.getHitTestResults(hitTestSource);

                        if (hitTestResults.length > 0) {
                            const hit = hitTestResults[0];
                            const pose = hit.getPose(referenceSpace);

                            // Return the position of the plane as {x, y, z}
                            resolve({
                                x: pose.transform.position.x,
                                y: pose.transform.position.y,
                                z: pose.transform.position.z
                            });
                        }
                    }

                    renderer.setAnimationLoop(renderLoop);
                };

                renderer.setAnimationLoop(renderLoop);
            });
        } catch (error) {
            console.error('Error detecting the plane:', error);
            throw error;
        }
    }

    /**
     * Handles window resize events to adjust the renderer and camera.
     * Updates canvas dimensions and recalculates the camera's aspect ratio.
     */
    onWindowResize() {
        const { width, height } = this.canvas;
        this.canvasDimensions.width = width;
        this.canvasDimensions.height = height;

        this.camera.aspect = width / height;
        this.camera.updateProjectionMatrix();
        this.renderer.setSize(width, height);
    }

    createSceneSubjects(scene) {
        // Add a cube
        const geometry = new THREE.BoxGeometry();
        const material = new THREE.MeshBasicMaterial({ color: 0x00ff00 });
        const cube = new THREE.Mesh(geometry, material);
        scene.add(cube);

        return [cube];
    }
}