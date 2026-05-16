/* ══════════════════════════════════════
    Mapping état → labels UI
 ══════════════════════════════════════ */
 const STATUS_MAP = {
   idle:      { label: "Standby",   orb: "Dreaming" },
   active:    { label: "Online",    orb: "Listening" },
   speaking:  { label: "Speaking",  orb: "Blabla..." },
   off:       { label: "Offline", orb: "Offline" },
 };

 /* ══════════════════════════════════════
    Callbacks appelés depuis Python via evaluate_js()
 ══════════════════════════════════════ */

 /** Met à jour l'état visuel global. */
 function uiSetStatus(status) {
   const box  = document.getElementById("status-box");
   const info = document.getElementById("status-info");
   const orb   = document.getElementById("orb");
   const orbLb = document.getElementById("orb-info");

   box.dataset.s = status;
   orb.dataset.s  = status;

   const map = STATUS_MAP[status] || STATUS_MAP.off;
   info.textContent = map.label;
   orbLb.textContent = map.orb;

   // Activer/désactiver les boutons
   const running = (status !== "off");
   document.getElementById("btn-start").disabled = running;
   document.getElementById("btn-stop").disabled  = !running;
   document.getElementById("user-input").disabled = !running;
 }

 /* ══════════════════════════════════════
    Actions JS → Python
 ══════════════════════════════════════ */

 async function demarrer() {
   const btn = document.getElementById("btn-start");
   btn.classList.add("loading");
   btn.disabled = true;
   
   try {
     await window.pywebview.api.demarrer();
   } catch(e) {
     console.error("Erreur de communication lors du démarrage :", e);
   }
   
   btn.classList.remove("loading");
 }

 async function arreter() {
   const btn = document.getElementById("btn-stop");
   btn.classList.add("loading");
   
   try {
     await window.pywebview.api.arreter();
   } catch(e) {
     console.error("Erreur de communication lors de l'arrêt :", e);
   }
   
   btn.classList.remove("loading");
 }

function gererEntree(event) {
    // Si la touche pressée est "Enter" (Entrée)
    if (event.key === "Enter") {
      const inputField = document.getElementById('user-input');
      const commande = inputField.value;

      // On vérifie que le champ n'est pas vide
      if (commande.trim() !== "") {
        // Envoi à l'API Python (SaphirAPI)
        pywebview.api.envoyer_texte(commande).then(function(response) {
          console.log("Réponse de Python:", response);
        });
        
        // Suppression immédiate du texte dans le champ après la validation
        inputField.value = "";
      }
    }
  }

