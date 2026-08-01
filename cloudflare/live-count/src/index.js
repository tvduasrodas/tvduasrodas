const ALLOWED_ORIGINS = new Set([
    "https://tvduasrodas.com",
    "https://www.tvduasrodas.com"
]);

export default {
    fetch(request, env) {
        const url = new URL(request.url);
        if (url.pathname !== "/live") return new Response("Not found", { status: 404 });
        const origin = request.headers.get("Origin");
        if (!ALLOWED_ORIGINS.has(origin)) return new Response("Forbidden", { status: 403 });
        if (request.headers.get("Upgrade") !== "websocket") {
            return new Response("WebSocket required", { status: 426 });
        }
        return env.LIVE_ROOM.getByName("current-live").fetch(request);
    }
};

export class LiveRoom {
    constructor(ctx) {
        this.ctx = ctx;
    }

    async fetch() {
        const pair = new WebSocketPair();
        const client = pair[0];
        const server = pair[1];
        this.ctx.acceptWebSocket(server);
        server.serializeAttachment({ viewerId: "", active: false });
        this.broadcastCount();
        return new Response(null, { status: 101, webSocket: client });
    }

    webSocketMessage(ws, message) {
        try {
            const data = JSON.parse(message);
            if (data.type !== "presence" || typeof data.viewerId !== "string") return;
            const viewerId = data.viewerId.slice(0, 100);
            if (!viewerId) return;
            ws.serializeAttachment({ viewerId, active: data.active === true });
            this.broadcastCount();
        } catch (_) {}
    }

    webSocketClose() {
        this.broadcastCount();
    }

    webSocketError() {
        this.broadcastCount();
    }

    broadcastCount() {
        const sockets = this.ctx.getWebSockets();
        const activeViewers = new Set();
        for (const socket of sockets) {
            const presence = socket.deserializeAttachment();
            if (presence && presence.active && presence.viewerId) activeViewers.add(presence.viewerId);
        }
        const payload = JSON.stringify({ type: "count", count: activeViewers.size });
        for (const socket of sockets) {
            try { socket.send(payload); } catch (_) {}
        }
    }
}
