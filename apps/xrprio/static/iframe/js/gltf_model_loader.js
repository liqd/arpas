import * as THREE from 'https://cdnjs.cloudflare.com/ajax/libs/three.js/110/three.module.js';
// import { GLTFLoader } from 'https://cdnjs.cloudflare.com/ajax/libs/three.js/r110/examples/jsm/loaders/GLTFLoader.js';
import { GLTFLoader } from 'https://cdn.jsdelivr.net/npm/three@0.110/examples/jsm/loaders/GLTFLoader.js';

/**
 * Loads a GLTF model into the provided scene using the given URL.
 * @param {THREE.Scene} scene - The Three.js scene where the model will be added.
 * @param {string} url - The URL or file path of the GLTF model.
 * @returns {Promise<THREE.Object3D>} - A promise that resolves to the loaded model.
 */
export function loadGLTFModel(scene, url, 
    position = { x: 0, y: 0, z: 0 }, 
    rotation = { x: 0, y: 0, z: 0 },
    scale = { x: 1, y: 1, z: 1 }) {
    const loader = new GLTFLoader();
    const textureLoader = new THREE.TextureLoader();
    const texture = textureLoader.load('/static/iframe/gltf_models/bench/textures/lambert1_baseColor.png');

    return new Promise((resolve, reject) => {
        loader.load(
            url,
            (gltf) => {
                const model = gltf.scene;
                
                // Traverse the model and apply the texture to meshes
                model.traverse((child) => {
                    if (child.isMesh) {
                        child.material.map = texture; // Assign the texture to the material's map
                        child.material.needsUpdate = true; // Ensure the material is updated
                    }
                });
                
                scene.add(model);
                setModelPosition(model, position); // Set position
                setModelRotation(model, rotation); // Set rotation
                setModelScale(model, scale); // Set scale

                resolve(model); // Resolve the promise with the loaded model
            },
            (xhr) => {
                console.log(`${(xhr.loaded / xhr.total * 100).toFixed(2)}% loaded`);
            },
            (error) => {
                console.error('An error occurred:', error);
                reject(error); // Reject the promise with the error
            }
        );
    });
}


/**
 * Sets the position of a model.
 * @param {THREE.Object3D} model - The loaded model whose position needs to be updated.
 * @param {Object} position - An object containing x, y, and z coordinates.
 * @param {number} position.x - The x-coordinate for the model's position.
 * @param {number} position.y - The y-coordinate for the model's position.
 * @param {number} position.z - The z-coordinate for the model's position.
 */
export function setModelPosition(model, position) {
    if (model && position) {
        model.position.set(position.x, position.y, position.z);
    } else {
        console.error('Invalid model or position data.');
    }
}
/**
 * Sets the rotation of a model.
 * @param {THREE.Object3D} model - The loaded model whose rotation needs to be updated.
 * @param {Object} rotation - An object containing x, y, and z rotation angles in radians.
 * @param {number} rotation.x - The rotation angle around the x-axis, in radians.
 * @param {number} rotation.y - The rotation angle around the y-axis, in radians.
 * @param {number} rotation.z - The rotation angle around the z-axis, in radians.
 */
export function setModelRotation(model, rotation) {
    if (model && rotation) {
        model.rotation.set(rotation.x, rotation.y, rotation.z);
    } else {
        console.error('Invalid model or rotation data.');
    }
}
/**
 * Sets the scale of a model.
 * @param {THREE.Object3D} model - The loaded model whose scale needs to be updated.
 * @param {Object} scale - An object containing x, y, and z scale factors.
 * @param {number} scale.x - The scale factor along the x-axis.
 * @param {number} scale.y - The scale factor along the y-axis.
 * @param {number} scale.z - The scale factor along the z-axis.
 */
export function setModelScale(model, scale) {
    if (model && scale) {
        model.scale.set(scale.x, scale.y, scale.z);
    } else {
        console.error('Invalid model or scale data.');
    }
}
