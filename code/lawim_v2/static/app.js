const state = {
  token: localStorage.getItem("lawim.token") || "",
  bootstrap: null,
  health: null,
  selectedConversationId: null,
};

const refs = {};

function byId(id) {
  return document.getElementById(id);
}

function cacheRefs() {
  Object.assign(refs, {
    runtimeChip: byId("runtime-chip"),
    currentUser: byId("current-user"),
    notice: byId("notice"),
    bootstrapSummary: byId("bootstrap-summary"),
    statusStrip: byId("status-strip"),
    organizationsList: byId("organizations-list"),
    propertiesList: byId("properties-list"),
    matchesList: byId("matches-list"),
    conversationsList: byId("conversations-list"),
    conversationDetail: byId("conversation-detail"),
    messageForm: byId("message-form"),
    loginForm: byId("login-form"),
    loginEmail: byId("login-email"),
    loginPassword: byId("login-password"),
    logoutButton: byId("logout-button"),
    demoButton: byId("use-demo-button"),
    matchForm: byId("match-form"),
    propertyForm: byId("property-form"),
    ownerOrganizationSelect: byId("owner-organization-select"),
  });
}

function setNotice(message, tone = "neutral") {
  refs.notice.dataset.tone = tone;
  refs.notice.textContent = message;
}

function setRuntimeChip(message, tone = "neutral") {
  refs.runtimeChip.dataset.tone = tone;
  refs.runtimeChip.textContent = message;
}

function money(value, currency = "XAF") {
  if (value === null || value === undefined || value === "") {
    return "n/a";
  }
  const formatted = new Intl.NumberFormat("fr-FR", {
    maximumFractionDigits: 0,
  }).format(Number(value));
  return `${formatted} ${currency}`;
}

function requestHeaders(headers = {}, auth = false) {
  const merged = { ...headers };
  if (auth && state.token) {
    merged.Authorization = `Bearer ${state.token}`;
  }
  return merged;
}

async function api(path, { method = "GET", auth = false, body = null, query = null, headers = {} } = {}) {
  const url = new URL(path, window.location.origin);
  if (query) {
    for (const [key, value] of Object.entries(query)) {
      if (value !== undefined && value !== null && `${value}`.trim() !== "") {
        url.searchParams.set(key, String(value));
      }
    }
  }

  const response = await fetch(url, {
    method,
    headers: requestHeaders({ ...(body ? { "Content-Type": "application/json" } : {}), ...headers }, auth),
    body: body ? JSON.stringify(body) : undefined,
  });

  const text = await response.text();
  let payload = {};
  if (text) {
    try {
      payload = JSON.parse(text);
    } catch (error) {
      throw new Error(`Invalid JSON response from ${path}`);
    }
  }

  if (!response.ok) {
    const message = payload?.error?.message || payload?.message || `HTTP ${response.status}`;
    throw new Error(message);
  }

  return payload;
}

function clearNode(node) {
  while (node.firstChild) {
    node.removeChild(node.firstChild);
  }
}

function renderStat(label, value, accent = "") {
  const item = document.createElement("article");
  item.className = "stat-card";
  if (accent) {
    item.dataset.accent = accent;
  }
  item.innerHTML = `<span class="stat-label">${label}</span><strong>${value}</strong>`;
  return item;
}

function renderSummary(summary) {
  clearNode(refs.statusStrip);
  const cards = [
    ["Organizations", summary.organizations ?? 0, "teal"],
    ["Users", summary.users ?? 0, "gold"],
    ["Published properties", summary.published_properties ?? 0, "violet"],
    ["Conversations", summary.conversations ?? 0, "coral"],
    ["Messages", summary.messages ?? 0, "sea"],
    ["Media", summary.media ?? 0, "slate"],
  ];
  cards.forEach(([label, value, accent]) => refs.statusStrip.appendChild(renderStat(label, value, accent)));
}

function renderList(target, items, renderer, emptyText) {
  clearNode(target);
  if (!items || !items.length) {
    const empty = document.createElement("p");
    empty.className = "muted empty-state";
    empty.textContent = emptyText;
    target.appendChild(empty);
    return;
  }
  items.forEach((item) => target.appendChild(renderer(item)));
}

function renderOrganizations(items) {
  renderList(refs.organizationsList, items, (organization) => {
    const article = document.createElement("article");
    article.className = "mini-card";
    article.innerHTML = `
      <div class="mini-card__header">
        <strong>${organization.name}</strong>
        <span class="chip subtle">${organization.kind}</span>
      </div>
      <p class="muted">${organization.slug}</p>
      <p>${organization.city || "No city"} · ${organization.user_count ?? 0} users</p>
    `;
    return article;
  }, "No organizations available.");

  const options = ["<option value=\"\">None</option>"]
    .concat(
      items.map((organization) =>
        `<option value="${organization.id}">${organization.name}</option>`,
      ),
    )
    .join("");
  refs.ownerOrganizationSelect.innerHTML = options;
}

function renderProperties(items) {
  renderList(refs.propertiesList, items, (property) => {
    const article = document.createElement("article");
    article.className = "mini-card mini-card--property";
    article.innerHTML = `
      <div class="mini-card__header">
        <strong>${property.title}</strong>
        <span class="chip subtle">${property.property_type}</span>
      </div>
      <p class="muted">${property.city}, ${property.country}</p>
      <p>${money(property.price_min, property.currency)} - ${money(property.price_max, property.currency)}</p>
      <p class="muted">Owner: ${property.owner_organization_name || "n/a"} · Media: ${property.media_count ?? 0} · Threads: ${property.conversation_count ?? 0}</p>
      <p>${property.summary}</p>
    `;
    return article;
  }, "No properties available.");
}

function renderMatches(items) {
  renderList(refs.matchesList, items, (match) => {
    const property = match.property;
    const article = document.createElement("article");
    article.className = "mini-card mini-card--match";
    article.innerHTML = `
      <div class="mini-card__header">
        <strong>${property.title}</strong>
        <span class="chip accent">${match.score}</span>
      </div>
      <p class="muted">${property.city}, ${property.country}</p>
      <p>${money(property.price_min, property.currency)} - ${money(property.price_max, property.currency)}</p>
      <p class="muted">${(match.reasons || []).join(" · ") || "No reasons returned."}</p>
    `;
    return article;
  }, "No match results yet.");
}

function renderConversationDetail(conversation) {
  const messages = conversation.messages || [];
  refs.conversationDetail.innerHTML = `
    <div class="detail-summary">
      <div>
        <p class="eyebrow">${conversation.status}</p>
        <h3>${conversation.subject}</h3>
        <p class="muted">
          Requester: ${conversation.requester_name || "n/a"} · Property: ${conversation.property_title || "n/a"}
        </p>
      </div>
      <div class="detail-badge">
        <span>Messages</span>
        <strong>${conversation.message_count ?? messages.length}</strong>
      </div>
    </div>
    <div class="message-stream">
      ${messages
        .map(
          (message) => `
            <article class="message">
              <div class="message__meta">
                <strong>${message.sender_name}</strong>
                <span class="muted">${message.created_at}</span>
              </div>
              <p>${message.body}</p>
            </article>
          `,
        )
        .join("")}
    </div>
  `;
  refs.messageForm.classList.toggle("hidden", !state.token);
}

function renderConversations(items) {
  renderList(refs.conversationsList, items, (conversation) => {
    const article = document.createElement("article");
    article.className = "mini-card mini-card--conversation";
    if (conversation.id === state.selectedConversationId) {
      article.dataset.active = "true";
    }
    article.innerHTML = `
      <div class="mini-card__header">
        <strong>${conversation.subject}</strong>
        <span class="chip subtle">${conversation.status}</span>
      </div>
      <p class="muted">${conversation.requester_name || "n/a"} · ${conversation.property_title || "n/a"}</p>
      <p>${conversation.last_message || "No messages yet."}</p>
    `;
    article.addEventListener("click", () => selectConversation(conversation.id));
    return article;
  }, "No conversations available.");
}

function renderHealth(health) {
  const environment = health.environment || {};
  setRuntimeChip(`${health.status.toUpperCase()} · ${environment.app_env || "unknown"}`, health.status === "ok" ? "ok" : "warn");
  refs.bootstrapSummary.textContent = `Database ${health.database?.path || "n/a"} · ${health.summary?.events ?? 0} events logged.`;
}

function renderBootstrap(payload) {
  state.bootstrap = payload;
  const currentUser = payload.current_user;

  if (currentUser) {
    refs.currentUser.textContent = `${currentUser.full_name} · ${currentUser.email}`;
    refs.logoutButton.disabled = false;
  } else {
    refs.currentUser.textContent = "Guest session";
    refs.logoutButton.disabled = !state.token;
  }

  renderSummary(payload.summary || {});
  renderOrganizations(payload.organizations || []);
  renderProperties(payload.properties || []);
  renderMatches(payload.matches || []);
  renderConversations(payload.conversations || []);

  if (state.token && !currentUser) {
    state.token = "";
    localStorage.removeItem("lawim.token");
    refs.currentUser.textContent = "Guest session";
    refs.logoutButton.disabled = true;
  }

  if (!state.selectedConversationId && (payload.conversations || []).length) {
    selectConversation(payload.conversations[0].id);
  } else if (state.selectedConversationId) {
    const current = (payload.conversations || []).find((conversation) => conversation.id === state.selectedConversationId);
    if (current) {
      selectConversation(current.id);
    } else {
      state.selectedConversationId = null;
      refs.conversationDetail.innerHTML = '<p class="muted">No conversation selected.</p>';
    }
  }
}

async function selectConversation(conversationId) {
  state.selectedConversationId = conversationId;
  const payload = await api(`/api/conversations/${conversationId}`);
  renderConversationDetail(payload.conversation);
  renderConversations(state.bootstrap?.conversations || []);
}

function parseNumber(value) {
  if (value === "" || value === null || value === undefined) {
    return null;
  }
  const parsed = Number(value);
  return Number.isFinite(parsed) ? parsed : null;
}

async function refresh() {
  try {
    setNotice("Refreshing runtime state...");
    const [health, bootstrap] = await Promise.all([
      api("/api/health"),
      api("/api/bootstrap", { auth: Boolean(state.token) }),
    ]);
    state.health = health;
    renderHealth(health);
    renderBootstrap(bootstrap);
    setNotice("Runtime is available, seeded and ready.");
  } catch (error) {
    setNotice(error.message, "error");
    setRuntimeChip("DEGRADED", "warn");
  }
}

async function handleLogin(event) {
  event.preventDefault();
  try {
    const email = refs.loginEmail.value.trim();
    const password = refs.loginPassword.value;
    const payload = await api("/api/auth/login", {
      method: "POST",
      body: { email, password },
    });
    state.token = payload.token;
    localStorage.setItem("lawim.token", state.token);
    setNotice(`Authenticated as ${payload.user.email}`, "success");
    await refresh();
  } catch (error) {
    setNotice(error.message, "error");
  }
}

async function handleLogout() {
  try {
    if (state.token) {
      await api("/api/auth/logout", { method: "POST", auth: true });
    }
  } catch (error) {
    console.warn("Logout warning:", error);
  } finally {
    state.token = "";
    localStorage.removeItem("lawim.token");
    refs.messageForm.classList.add("hidden");
    refs.conversationDetail.innerHTML = '<p class="muted">No conversation selected.</p>';
    state.selectedConversationId = null;
    setNotice("Session cleared.", "neutral");
    await refresh();
  }
}

async function handleMatchSearch(event) {
  event.preventDefault();
  try {
    const form = new FormData(refs.matchForm);
    const payload = await api("/api/matches", {
      query: {
        city: form.get("city"),
        budget_min: parseNumber(form.get("budget_min")),
        budget_max: parseNumber(form.get("budget_max")),
        latitude: parseNumber(form.get("latitude")),
        longitude: parseNumber(form.get("longitude")),
        limit: parseNumber(form.get("limit")),
      },
    });
    renderMatches(payload.matches || []);
    setNotice(`Returned ${payload.matches?.length || 0} ranked matches.`, "success");
  } catch (error) {
    setNotice(error.message, "error");
  }
}

async function handlePropertyCreate(event) {
  event.preventDefault();
  if (!state.token) {
    setNotice("Authenticate before creating records.", "error");
    return;
  }
  try {
    const form = new FormData(refs.propertyForm);
    await api("/api/properties", {
      method: "POST",
      auth: true,
      body: {
        title: form.get("title"),
        summary: form.get("summary"),
        city: form.get("city"),
        property_type: form.get("property_type"),
        price_min: parseNumber(form.get("price_min")),
        price_max: parseNumber(form.get("price_max")),
        latitude: parseNumber(form.get("latitude")),
        longitude: parseNumber(form.get("longitude")),
        owner_organization_id: parseNumber(form.get("owner_organization_id")),
      },
    });
    refs.propertyForm.reset();
    setNotice("Property created and persisted.", "success");
    await refresh();
  } catch (error) {
    setNotice(error.message, "error");
  }
}

async function handleMessageCreate(event) {
  event.preventDefault();
  if (!state.token || !state.selectedConversationId) {
    setNotice("Select a conversation and authenticate first.", "error");
    return;
  }
  try {
    const form = new FormData(refs.messageForm);
    await api(`/api/conversations/${state.selectedConversationId}/messages`, {
      method: "POST",
      auth: true,
      body: {
        body: form.get("body"),
      },
    });
    refs.messageForm.reset();
    setNotice("Reply sent.", "success");
    await selectConversation(state.selectedConversationId);
  } catch (error) {
    setNotice(error.message, "error");
  }
}

function populateDemoCredentials() {
  refs.loginEmail.value = "admin@lawim.local";
  refs.loginPassword.value = "lawim-demo";
}

function bindEvents() {
  refs.loginForm.addEventListener("submit", handleLogin);
  refs.logoutButton.addEventListener("click", handleLogout);
  refs.demoButton.addEventListener("click", populateDemoCredentials);
  refs.matchForm.addEventListener("submit", handleMatchSearch);
  refs.propertyForm.addEventListener("submit", handlePropertyCreate);
  refs.messageForm.addEventListener("submit", handleMessageCreate);
}

document.addEventListener("DOMContentLoaded", async () => {
  cacheRefs();
  bindEvents();
  populateDemoCredentials();
  await refresh();
});
