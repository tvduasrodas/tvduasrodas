(function () {
    "use strict";

    const API_URL = "wss://live-count.tvduasrodas.com/live";
    const RECONNECT_DELAY = 3000;
    const PLAYER_PLAYING = 1;
    let player = null;
    let socket = null;
    let liveEnabled = false;
    let playing = false;
    let playerInView = false;
    let reconnectTimer = null;

    function viewerId() {
        const key = "tdr-live-viewer-id";
        let id = localStorage.getItem(key);
        if (!id) {
            id = crypto.randomUUID ? crypto.randomUUID() : `${Date.now()}-${Math.random()}`;
            localStorage.setItem(key, id);
        }
        return id;
    }

    function counterElements() {
        return document.querySelectorAll("[data-live-viewers]");
    }

    function render(count) {
        counterElements().forEach((element) => {
            element.hidden = !liveEnabled;
            const number = element.querySelector("[data-live-viewers-count]");
            const label = element.querySelector("[data-live-viewers-label]");
            if (number) number.textContent = new Intl.NumberFormat("pt-BR").format(count);
            if (label) label.textContent = count === 1 ? "pessoa assistindo agora" : "pessoas assistindo agora";
        });
    }

    function sendPresence() {
        if (!socket || socket.readyState !== WebSocket.OPEN) return;
        const active = liveEnabled && playing && playerInView && document.visibilityState === "visible";
        socket.send(JSON.stringify({ type: "presence", viewerId: viewerId(), active }));
    }

    function connect() {
        if (!liveEnabled || socket) return;
        try {
            socket = new WebSocket(API_URL);
            socket.addEventListener("open", sendPresence);
            socket.addEventListener("message", (event) => {
                try {
                    const data = JSON.parse(event.data);
                    if (data.type === "count" && Number.isFinite(data.count)) render(data.count);
                } catch (_) {}
            });
            socket.addEventListener("close", () => {
                socket = null;
                if (liveEnabled) reconnectTimer = setTimeout(connect, RECONNECT_DELAY);
            });
            socket.addEventListener("error", () => socket && socket.close());
        } catch (_) {
            reconnectTimer = setTimeout(connect, RECONNECT_DELAY);
        }
    }

    function loadYouTubeApi(callback) {
        if (window.YT && window.YT.Player) return callback();
        const previous = window.onYouTubeIframeAPIReady;
        window.onYouTubeIframeAPIReady = function () {
            if (typeof previous === "function") previous();
            callback();
        };
        if (!document.querySelector('script[src="https://www.youtube.com/iframe_api"]')) {
            const script = document.createElement("script");
            script.src = "https://www.youtube.com/iframe_api";
            document.head.appendChild(script);
        }
    }

    function watchPlayer(iframe) {
        if (!iframe || player) return;
        loadYouTubeApi(() => {
            player = new YT.Player(iframe, {
                events: {
                    onReady(event) {
                        playing = event.target.getPlayerState() === PLAYER_PLAYING;
                        sendPresence();
                    },
                    onStateChange(event) {
                        playing = event.data === PLAYER_PLAYING;
                        sendPresence();
                    }
                }
            });
            const observer = new IntersectionObserver((entries) => {
                playerInView = entries[0]?.isIntersecting && entries[0].intersectionRatio >= 0.35;
                sendPresence();
            }, { threshold: [0, 0.35] });
            observer.observe(iframe);
        });
    }

    document.addEventListener("visibilitychange", sendPresence);

    window.TDRLiveViewers = {
        start(iframe) {
            liveEnabled = true;
            render(0);
            connect();
            watchPlayer(iframe);
        },
        stop() {
            liveEnabled = false;
            playing = false;
            clearTimeout(reconnectTimer);
            sendPresence();
            if (socket) socket.close();
            counterElements().forEach((element) => { element.hidden = true; });
        }
    };
})();
