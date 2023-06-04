import * as THREE from 'https://cdn.jsdelivr.net/npm/three@0.118/build/three.module.js';

import {OrbitControls} from 'https://cdn.jsdelivr.net/npm/three@0.118/examples/jsm/controls/OrbitControls.js';
import {STLLoader} from "https://cdn.jsdelivr.net/npm/three@0.118.3/examples/jsm/loaders/STLLoader.js";



const DDD_viewer = document.getElementById("3D_viewer");
const bouton = document.getElementById('Import_button');
const retract_button = document.getElementById('retract_button');
const angle = Math.PI / 20;
const info_Files = document.getElementById("Info_Files");
const log_messages = document.getElementById('Log_Messages');
const container = document.getElementById('container');
/*
axios.get('/data').then(function(response){
    const answer = response.data;
    console.log(answer);
    let encoder = new TextEncoder();
    let process_data = [];
    for (let i in answer){
        process_data.push(encoder.encode(atob(answer[i]['00420011'].InlineBinary)));
    }


});
*/
axios.get('/data').then(function(response){
    const answer = response.data;
    console.log(answer);
    let encoder = new TextEncoder();
    let process_data = [];
    for (let i in answer){
      load_info_python(answer[i])
	  var binarystring = atob(answer[i]['00420011'].InlineBinary);
	  var bytearray = new Uint8Array(binarystring.length );
	  for (var j = 0; j < binarystring.length; j += 1) {
  	     bytearray[j] = binarystring.charCodeAt(j);
	  }
        process_data.push(bytearray);
    }
    console.log(process_data);
    loadSTLModel(process_data);
});

bouton.addEventListener('click', () => {
    const input = document.createElement('input');
    input.type = 'file';
    input.multiple = true;

    input.addEventListener('change', () => {
        while (DDD_viewer.firstChild) {
            DDD_viewer.removeChild(DDD_viewer.firstChild);
        }
        while (info_Files.firstChild) {
            info_Files.removeChild(info_Files.firstChild);
        }
        log_messages.textContent = "";
        const files = input.files;
        let process_data = [];
        let check = 0;
        for (let i = 0; i < files.length; i++) {
            const file = files[i];

            if(file.name.endsWith(".dcm")) {
                const reader = new FileReader();
                reader.onload = () => {
                    const byteArray = new Uint8Array(reader.result);
                    const dataSet = dicomParser.parseDicom(byteArray);

                    const obElement = dataSet.elements['x00420011']; // Tag réel pour OB
                    if (obElement) {
                        load_info(dataSet);
                        const byteSlice = byteArray.slice(obElement.dataOffset, obElement.dataOffset + obElement.length);
                        process_data.push(byteSlice)
                    } else {
                        check++;
                        const text_sub = "le fichier : " + file.name +" ne contient pas de fichier Dicom Encapsulé. <br>"
                        log_messages.innerHTML +=  text_sub;
                    }


                    if (process_data.length === files.length - check) {
                        loadSTLModel(process_data);
                    }
                };
                reader.readAsArrayBuffer(file);
            }else{
                check++;
                const text_sub = "le fichier : " + file.name +" n'est pas un fichier Dicom. <br>"
                log_messages.innerHTML +=  text_sub;
            }
        }
    });
    input.click();
});

function loadSTL(byteSlice){
    const loader = new STLLoader();
    const geometry = loader.parse(byteSlice.buffer);
    //geometry.center();
    const material = new THREE.MeshStandardMaterial({
        color: 0xff0000,
        metalness: 0.35,   // between 0 and 1
        roughness: 0.5 // between 0 and 1
    });
    return new THREE.Mesh(geometry, material);
}

function loadSTLModel(data) {
    console.log(data);
    let STLS = [];
    const scene = new THREE.Scene();
    const renderer = new THREE.WebGLRenderer({antialias: true});
    for (let i = 0; i < data.length; i++) {
        console.log(data[i]);
        let sub = loadSTL(data[i]);
        STLS.push(sub);
        scene.add(sub);
    }

    const fov = 60;
    const aspect = 1920 / 1080;
    const near = 1.0;
    const far = 1000.0;
    const camera = new THREE.PerspectiveCamera(fov, aspect, near, far);

    scene.background = new THREE.Color(0x0000ff);

    const box = new THREE.Box3();
    for (let i = 0; i < STLS.length; i++) {
        box.expandByObject(STLS[i]);
    }
    const center = box.getCenter(new THREE.Vector3());

    for (let i = 0; i < STLS.length; i++) {
        STLS[i].position.sub(center);
    }

    camera.position.set(center.x, center.y, box.max.z + 50);
    camera.lookAt(center);

    renderer.render(scene,camera);
    renderer.setSize(window.innerWidth*0.85, window.innerHeight);
    DDD_viewer.appendChild(renderer.domElement);


    const controls = new OrbitControls(camera, renderer.domElement);
    controls.target.set(0, 20, 0);
    controls.update();

    scene.add( new THREE.AmbientLight( 0xffffff, 1 ) );

    const dirLight = new THREE.DirectionalLight( 0xffffff, 0.4 );
    dirLight.position.set( 150, 150, 150);
    scene.add( dirLight );

    const dirLight2 = new THREE.DirectionalLight( 0xffffff, 0.4 );
    dirLight2.position.set( -150, -150, 150);
    scene.add( dirLight2 );





    // Ajouter un écouteur d'événement pour les touches
    document.addEventListener('keydown', event => {
        switch (event.key) {
            case 'a':
                scene.rotateOnAxis(new THREE.Vector3(0, 0, 1), angle);
                break;
            case 'z':
                scene.rotateOnAxis(new THREE.Vector3(0, 0, -1), angle);
                break;
            case 'q':
                scene.rotateOnAxis(new THREE.Vector3(0, 1, 0), angle);
                break;
            case 's':
                scene.rotateOnAxis(new THREE.Vector3(0, -1, 0), angle);
                break;
            case 'w':
                scene.rotateOnAxis(new THREE.Vector3(1, 0, 0), angle);
                break;
            case 'x':
                scene.rotateOnAxis(new THREE.Vector3(-1, 0, 0), angle);
                break;
        }
    });

    // Créer une boucle d'animation pour rendre la scène en continu
    function render() {
        requestAnimationFrame(render);
        //controls.update();
        renderer.render(scene, camera);
    }

    let isCollapsed = false;

    retract_button.addEventListener("click", () => {
        if(isCollapsed){
            container.style.width = "250px";
            renderer.setSize(DDD_viewer.clientWidth-250, DDD_viewer.clientHeight);
            isCollapsed = false;
        }else{
            container.style.width = "0px";
            renderer.setSize(DDD_viewer.clientWidth+250, DDD_viewer.clientHeight);
            isCollapsed = true;
        }
    });
    render();
}

function load_info(dataSet){
    const childDiv = document.createElement('div');
    const button = document.createElement('button');
    button.innerHTML = '+/- '+dataSet.string('x00420010');
    const contentDiv = document.createElement('div');
    contentDiv.innerHTML += "<p style='font-weight: bold;padding-left: 10px'>Nom Du Fichier :</p>";
    contentDiv.innerHTML += "<p style='padding-left: 10px'>"+ dataSet.string('x00420010') +"</p>";

    childDiv.appendChild(button);
    childDiv.appendChild(contentDiv);
    childDiv.style.overflowY = 'auto';

    childDiv.style.borderTop= '1px solid black';
    info_Files.appendChild(childDiv);

    button.addEventListener('click', () => {
        if (childDiv.style.height === '20px') {
            childDiv.style.height = 'fit-content';
        } else {
            childDiv.style.height = '20px';
        }
    });
}

function load_info_python(dataSet){
    const childDiv = document.createElement('div');
    const button = document.createElement('button');
    button.innerHTML = '+/- '+dataSet['00420010'].Value;
    const contentDiv = document.createElement('div');
    contentDiv.innerHTML += "<p style='font-weight: bold;padding-left: 10px'>Nom Du Fichier :</p>";
    contentDiv.innerHTML += "<p style='padding-left: 10px'>"+dataSet['00420010'].Value +"</p>";

    childDiv.appendChild(button);
    childDiv.appendChild(contentDiv);
    childDiv.style.overflowY = 'auto';

    childDiv.style.borderTop= '1px solid black';
    info_Files.appendChild(childDiv);

    button.addEventListener('click', () => {
        if (childDiv.style.height === '20px') {
            childDiv.style.height = 'fit-content';
        } else {
            childDiv.style.height = '20px';
        }
    });
}