(function () {
    "use strict";

    function buttonFor(player) {
        if (!player?.id) return null;
        return document.querySelector(`[data-live-audio][data-player-id="${player.id}"]`);
    }

    function command(player, func, args = []) {
        player?.contentWindow?.postMessage(JSON.stringify({
            event: "command",
            func,
            args
        }), "*");
    }

    function activate(player) {
        command(player, "unMute");
        command(player, "setVolume", [100]);
        command(player, "playVideo");
        const button = buttonFor(player);
        if (button) button.hidden = true;
    }

    function show(player) {
        const button = buttonFor(player);
        if (button) button.hidden = false;
    }

    function hide(player) {
        const button = buttonFor(player);
        if (button) button.hidden = true;
    }

    document.addEventListener("click", (event) => {
        const button = event.target.closest("[data-live-audio]");
        if (!button) return;
        activate(document.getElementById(button.dataset.playerId));
    });

    window.TDRLiveAudio = { activate, show, hide };
})();
