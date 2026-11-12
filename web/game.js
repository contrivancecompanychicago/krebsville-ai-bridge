import * as THREE from "https://cdn.jsdelivr.net/npm/three@0.169.0/build/three.module.js";

const canvas = document.querySelector("#world");
const startPanel = document.querySelector("#start-panel");
const startButton = document.querySelector("#start-button");
const nameInput = document.querySelector("#player-name");
const startError = document.querySelector("#start-error");
const hud = document.querySelector("#hud");
const dialogue = document.querySelector("#dialogue");
const titleElement = document.querySelector("#scene-title");
const messageElement = document.querySelector("#scene-message");
const rosterElement = document.querySelector("#roster");
const choicesElement = document.querySelector("#choices");
const interactionPrompt = document.querySelector("#interaction-prompt");
const controlsHint = document.querySelector("#controls-hint");
const toast = document.querySelector("#toast");
const statsPanel = document.querySelector("#stats-panel");
const statsGrid = document.querySelector("#stats-grid");
const sessionBar = document.querySelector("#session-bar");
const sessionIdLabel = document.querySelector("#session-id");

const scene = new THREE.Scene();
scene.background = new THREE.Color(0x101820);
scene.fog = new THREE.Fog(0x101820, 12, 42);
const camera = new THREE.PerspectiveCamera(60, window.innerWidth / window.innerHeight, 0.1, 100);
const renderer = new THREE.WebGLRenderer({ canvas, antialias: true });
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.outputColorSpace = THREE.SRGBColorSpace;
renderer.toneMapping = THREE.ACESFilmicToneMapping;

scene.add(new THREE.HemisphereLight(0x9caec2, 0x171719, 2.0));
const moon = new THREE.DirectionalLight(0xa6c8ff, 2.0);
moon.position.set(-5, 12, 4);
moon.castShadow = true;
scene.add(moon);

const materials = {
  asphalt: new THREE.MeshStandardMaterial({ color: 0x252a2d, roughness: 0.92 }),
  brick: new THREE.MeshStandardMaterial({ color: 0x3e3332, roughness: 0.95 }),
  brickDark: new THREE.MeshStandardMaterial({ color: 0x292b2d, roughness: 0.95 }),
  concrete: new THREE.MeshStandardMaterial({ color: 0x56595a, roughness: 1 }),
  metal: new THREE.MeshStandardMaterial({ color: 0x4a5357, metalness: 0.7, roughness: 0.5 }),
  amber: new THREE.MeshStandardMaterial({ color: 0xffb35c, emissive: 0x9d4511, emissiveIntensity: 1.3 }),
  clinic: new THREE.MeshStandardMaterial({ color: 0x777878, roughness: 0.9 }),
};

const playerNameLabel = document.querySelector("#status");
let playerName = "Visitor";

function box(parent, name, size, position, material, options = {}) {
  const mesh = new THREE.Mesh(new THREE.BoxGeometry(...size), material);
  mesh.name = name;
  mesh.position.set(...position);
  mesh.castShadow = true;
  mesh.receiveShadow = true;
  if (options.choiceId) mesh.userData.choiceId = options.choiceId;
  if (options.interactable) mesh.userData.interactable = true;
  parent.add(mesh);
  return mesh;
}

box(scene, "wet alley", [12, 0.2, 42], [0, -0.15, -8], materials.asphalt);
box(scene, "left brick wall", [0.7, 8, 42], [-6, 3.8, -8], materials.brick);
box(scene, "right brick wall", [0.7, 8, 42], [6, 3.8, -8], materials.brickDark);
box(scene, "clinic facade", [10, 7, 1.1], [0, 3.35, -27], materials.clinic);
box(scene, "clinic door frame", [2.4, 3.5, 0.4], [0, 1.55, -26.3], materials.metal);
box(scene, "clinic door", [1.7, 3, 0.2], [0, 1.45, -26.0], materials.brickDark, { choiceId: "clinic", interactable: true });
box(scene, "clinic sign", [4, 0.7, 0.3], [0, 5.5, -26.2], materials.amber);
box(scene, "fire escape", [4, 0.15, 3], [-3.6, 4.5, -11], materials.metal);
box(scene, "fire escape rail", [4, 0.12, 0.12], [-3.6, 5.5, -12.4], materials.metal);

const rainCount = 520;
const rainPositions = new Float32Array(rainCount * 3);
for (let i = 0; i < rainCount; i++) {
  rainPositions[i * 3] = (Math.random() - 0.5) * 18;
  rainPositions[i * 3 + 1] = Math.random() * 12;
  rainPositions[i * 3 + 2] = -22 + Math.random() * 34;
}
const rainGeometry = new THREE.BufferGeometry();
rainGeometry.setAttribute("position", new THREE.BufferAttribute(rainPositions, 3));
const rain = new THREE.Points(rainGeometry, new THREE.PointsMaterial({ color: 0xb9c9d5, size: 0.045, transparent: true, opacity: 0.55 }));
scene.add(rain);

const radio = new THREE.Group();
radio.position.set(-2.2, 0.25, -2.0);
radio.userData.choiceId = "radio";
radio.userData.interactable = true;
box(radio, "radio body", [0.75, 0.48, 0.32], [0, 0.25, 0], materials.metal);
box(radio, "radio dial", [0.28, 0.12, 0.05], [0, 0.28, 0.19], materials.amber);
const antenna = new THREE.Mesh(new THREE.CylinderGeometry(0.025, 0.025, 0.7), materials.metal);
antenna.position.set(0.22, 0.85, 0);
antenna.rotation.z = -0.2;
antenna.castShadow = true;
radio.add(antenna);
scene.add(radio);

const hatch = new THREE.Group();
hatch.position.set(2.2, 0.015, 3.5);
hatch.userData.choiceId = "hatch";
hatch.userData.interactable = true;
const hatchPlate = new THREE.Mesh(new THREE.BoxGeometry(1.7, 0.12, 2), materials.metal);
hatchPlate.position.y = 0.06;
hatchPlate.rotation.y = -0.12;
hatchPlate.castShadow = true;
hatch.add(hatchPlate);
const hatchHandle = new THREE.Mesh(new THREE.TorusGeometry(0.16, 0.035, 8, 16), materials.amber);
hatchHandle.position.set(0.42, 0.15, 0);
hatchHandle.rotation.x = Math.PI / 2;
hatch.add(hatchHandle);
scene.add(hatch);

for (const z of [-17, -4, 9]) {
  box(scene, "dumpster", [2, 1.3, 1.2], [4.1, 0.6, z], materials.brickDark);
  box(scene, "dumpster lid", [2.1, 0.12, 1.3], [4.1, 1.3, z], materials.metal);
}

const player = new THREE.Group();
const coat = new THREE.MeshStandardMaterial({ color: 0x26373e, roughness: 0.8 });
const skin = new THREE.MeshStandardMaterial({ color: 0xa57962, roughness: 0.9 });
const torso = new THREE.Mesh(new THREE.CapsuleGeometry(0.32, 0.7, 4, 8), coat);
torso.position.y = 0.85;
torso.castShadow = true;
player.add(torso);
const head = new THREE.Mesh(new THREE.SphereGeometry(0.23, 16, 12), skin);
head.position.y = 1.52;
head.castShadow = true;
player.add(head);
player.position.set(0, 0, 5);
scene.add(player);

const keys = new Set();
const raycaster = new THREE.Raycaster();
const pointer = new THREE.Vector2();
const clock = new THREE.Clock();
let sessionId = null;
let activeScene = "arrival";
let activeChoices = [];
let locked = false;
let nearbyChoice = null;
let toastTimer;

function notify(text) {
  toast.textContent = text;
  toast.classList.remove("hidden");
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => toast.classList.add("hidden"), 2200);
}

function renderStats(stats) {
  const entries = [
    ["clarity", "Clarity"],
    ["trust", "Trust"],
    ["pressure", "Pressure"],
    ["resolve", "Resolve"],
  ];
  statsGrid.replaceChildren();
  for (const [key, label] of entries) {
    const item = document.createElement("div");
    item.className = "stat-item";
    item.innerHTML = `
      <span class="stat-label">${label}</span>
      <strong class="stat-value">${stats?.[key] ?? 0}</strong>
    `;
    statsGrid.append(item);
  }
}

function showStory(data, sceneId) {
  activeScene = sceneId;
  activeChoices = data.choices || [];
  titleElement.textContent = data.title || "Krebsville";
  messageElement.textContent = data.message || "The line has gone quiet.";
  playerName = data.player_name || playerName;
  playerNameLabel.textContent = `${playerName} · ${data.title || "Night Watch"}`;
  rosterElement.replaceChildren();
  for (const character of data.characters || []) {
    const badge = document.createElement("span");
    badge.className = `character-badge ${character.presence}`;
    badge.textContent = `${character.display_name} · ${character.presence}`;
    rosterElement.append(badge);
  }
  choicesElement.replaceChildren();
  for (const choice of activeChoices) {
    const button = document.createElement("button");
    button.className = "choice-button";
    button.textContent = choice.label;
    button.addEventListener("click", () => advance(choice));
    choicesElement.append(button);
  }
  dialogModeUpdate();
  if (data.stats) renderStats(data.stats);
  if (data.session_id) {
    sessionIdLabel.textContent = `${data.session_id.slice(0, 8)}…`;
    sessionIdLabel.title = data.session_id;
  }
}

function dialogModeUpdate() {
  dialogue.classList.remove("hidden");
  statsPanel.classList.remove("hidden");
  sessionBar.classList.remove("hidden");
  if (activeChoices.length === 0) {
    const restart = document.createElement("button");
    restart.className = "choice-button primary";
    restart.textContent = "Begin again";
    restart.addEventListener("click", () => startGame());
    choicesElement.append(restart);
  }
}

async function api(path, body) {
  const response = await fetch(path, {
    method: body ? "POST" : "GET",
    headers: body ? { "Content-Type": "application/json" } : undefined,
    body: body ? JSON.stringify(body) : undefined,
  });
  const data = await response.json();
  if (!response.ok) throw new Error(data.detail || "The city line is unavailable.");
  return data;
}

async function startGame() {
  startError.textContent = "";
  startButton.disabled = true;
  try {
    const playerNameInput = nameInput.value.trim() || "Visitor";
    const data = await api("/api/onboarding/start", {
      player_name: playerNameInput,
      source: "threejs",
    });
    sessionId = data.session_id;
    activeScene = "arrival";
    playerName = data.player_name || playerNameInput;
    startPanel.classList.add("hidden");
    hud.classList.remove("hidden");
    controlsHint.classList.remove("hidden");
    showStory(data, activeScene);
    notify("Find the radio, clinic door, or maintenance hatch.");
  } catch (error) {
    startError.textContent = error.message;
  } finally {
    startButton.disabled = false;
  }
}

async function advance(choice) {
  if (!sessionId || locked) return;
  locked = true;
  choicesElement.querySelectorAll("button").forEach((button) => { button.disabled = true; });
  try {
    const data = await api("/api/onboarding/advance", { session_id: sessionId, choice_id: choice.id });
    showStory(data, choice.next_scene || activeScene);
    notify(choice.next_scene === "dispatch" ? "A municipal line is calling." : "The alley gives way to another lead.");
  } catch (error) {
    notify(error.message);
    choicesElement.querySelectorAll("button").forEach((button) => { button.disabled = false; });
  } finally {
    locked = false;
  }
}

function interact(choiceId) {
  const choice = activeChoices.find((item) => item.id === choiceId);
  if (choice) advance(choice);
}

startButton.addEventListener("click", startGame);
nameInput.addEventListener("keydown", (event) => { if (event.key === "Enter") startGame(); });
window.addEventListener("keydown", (event) => {
  if (["KeyW", "KeyA", "KeyS", "KeyD", "ArrowUp", "ArrowDown", "ArrowLeft", "ArrowRight"].includes(event.code)) {
    keys.add(event.code);
    event.preventDefault();
  }
  if (event.code === "KeyE" && nearbyChoice) interact(nearbyChoice);
});
window.addEventListener("keyup", (event) => keys.delete(event.code));
window.addEventListener("blur", () => keys.clear());

canvas.addEventListener("pointerdown", (event) => {
  pointer.x = (event.clientX / window.innerWidth) * 2 - 1;
  pointer.y = -(event.clientY / window.innerHeight) * 2 + 1;
  raycaster.setFromCamera(pointer, camera);
  const hits = raycaster.intersectObjects([radio, hatch, scene.getObjectByName("clinic door")], true);
  for (const hit of hits) {
    let target = hit.object;
    while (target && !target.userData.choiceId) target = target.parent;
    if (target?.userData.choiceId) {
      if (target.position.distanceTo(player.position) < 6 || target === scene.getObjectByName("clinic door")) {
        interact(target.userData.choiceId);
      } else {
        notify("Move closer to investigate.");
      }
      break;
    }
  }
});

function updatePlayer(delta) {
  if (!sessionId || document.activeElement === nameInput) return;
  const x = (keys.has("KeyD") || keys.has("ArrowRight") ? 1 : 0) - (keys.has("KeyA") || keys.has("ArrowLeft") ? 1 : 0);
  const z = (keys.has("KeyS") || keys.has("ArrowDown") ? 1 : 0) - (keys.has("KeyW") || keys.has("ArrowUp") ? 1 : 0);
  const direction = new THREE.Vector3(x, 0, z);
  if (direction.lengthSq()) {
    direction.normalize();
    player.position.addScaledVector(direction, delta * 4.2);
    player.position.x = THREE.MathUtils.clamp(player.position.x, -4.8, 4.8);
    player.position.z = THREE.MathUtils.clamp(player.position.z, -24, 8);
    player.rotation.y = Math.atan2(direction.x, direction.z);
    torso.position.y = 0.85 + Math.sin(performance.now() * 0.012) * 0.035;
  }

  nearbyChoice = null;
  let nearest = Infinity;
  for (const object of [radio, hatch]) {
    const distance = object.position.distanceTo(player.position);
    if (distance < nearest && distance < 2.8 && activeChoices.some((choice) => choice.id === object.userData.choiceId)) {
      nearbyChoice = object.userData.choiceId;
      nearest = distance;
    }
  }
  const clinicDistance = new THREE.Vector3(0, 0, -26).distanceTo(player.position);
  if (clinicDistance < nearest && clinicDistance < 5 && activeChoices.some((choice) => choice.id === "clinic")) {
    nearbyChoice = "clinic";
  }
  interactionPrompt.classList.toggle("hidden", !nearbyChoice || !sessionId);

  const desiredCamera = new THREE.Vector3(player.position.x, player.position.y + 3.5, player.position.z + 7.5);
  camera.position.lerp(desiredCamera, 1 - Math.exp(-delta * 4));
  camera.lookAt(player.position.x, player.position.y + 1, player.position.z - 1.5);
}

function animate() {
  requestAnimationFrame(animate);
  const delta = Math.min(clock.getDelta(), 0.05);
  updatePlayer(delta);
  const positions = rain.geometry.attributes.position;
  for (let i = 0; i < rainCount; i++) {
    const y = positions.getY(i) - delta * 8;
    positions.setY(i, y < 0 ? 11 : y);
    positions.setZ(i, positions.getZ(i) + delta * 1.1);
    if (positions.getZ(i) > 12) positions.setZ(i, -25);
  }
  positions.needsUpdate = true;
  renderer.render(scene, camera);
}
animate();

window.addEventListener("resize", () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
});

renderStats({ clarity: 0, trust: 0, pressure: 0, resolve: 0 });
