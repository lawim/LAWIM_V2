const state = {
  token: localStorage.getItem("lawim.token") || "",
  bootstrap: null,
  health: null,
  activeJourney: localStorage.getItem("lawim.journey") || "buyer",
  selectedConversationId: null,
  selectedPropertyId: null,
  selectedPropertyVersion: null,
  selectedPropertyTitle: null,
  selectedProjectId: null,
  refreshInFlight: false,
};

const refs = {};
const moneyFormatter = new Intl.NumberFormat("fr-FR", {
  maximumFractionDigits: 0,
});

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
    mediaList: byId("media-list"),
    matchesList: byId("matches-list"),
    conversationsList: byId("conversations-list"),
    notificationsList: byId("notifications-list"),
    markNotificationsReadButton: byId("mark-notifications-read"),
    conversationDetail: byId("conversation-detail"),
    messageForm: byId("message-form"),
    loginForm: byId("login-form"),
    loginEmail: byId("login-email"),
    loginPassword: byId("login-password"),
    logoutButton: byId("logout-button"),
    demoButton: byId("use-demo-button"),
    matchForm: byId("match-form"),
    propertyForm: byId("property-form"),
    geoForm: byId("geo-form"),
    geoResult: byId("geo-result"),
    mediaUploadForm: byId("media-upload-form"),
    mediaPropertySelect: byId("media-property-select"),
    ownerOrganizationSelect: byId("owner-organization-select"),
    registerOrganizationSelect: byId("register-organization-select"),
    adminOrganizationSelect: byId("admin-organization-select"),
    journeyNav: byId("journey-nav"),
    registerForm: byId("register-form"),
    propertySearchForm: byId("property-search-form"),
    propertySearchMeta: byId("property-search-meta"),
    notificationFilterForm: byId("notification-filter-form"),
    notificationUnreadCount: byId("notification-unread-count"),
    negotiationForm: byId("negotiation-form"),
    buyerConversationForm: byId("buyer-conversation-form"),
    adminOrgForm: byId("admin-org-form"),
    adminUserForm: byId("admin-user-form"),
    adminDashboard: byId("admin-dashboard"),
    selectedPropertyLabel: byId("selected-property-label"),
    publishPropertyButton: byId("publish-property-button"),
    archivePropertyButton: byId("archive-property-button"),
    projectForm: byId("project-form"),
    projectsList: byId("projects-list"),
    projectDetail: byId("project-detail"),
    partnersList: byId("partners-list"),
    servicesList: byId("services-list"),
  });
}

function setNotice(message, tone = "neutral", code = "") {
  refs.notice.dataset.tone = tone;
  refs.notice.textContent = code ? `[${code}] ${message}` : message;
}

function escapeHtml(value) {
  return String(value ?? "")
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#39;");
}

function setLoading(isLoading, message = "Loading...") {
  document.body.dataset.loading = isLoading ? "true" : "false";
  if (isLoading && refs.notice) {
    refs.notice.dataset.tone = "neutral";
    refs.notice.textContent = message;
  }
}

function formatApiError(payload, status) {
  const code = payload?.error?.code;
  const message = payload?.error?.message || payload?.message || `HTTP ${status}`;
  return { code: code || "", message };
}

function statusChipClass(status) {
  const normalized = String(status || "draft").toLowerCase();
  if (normalized === "published") {
    return "chip accent";
  }
  if (normalized === "archived") {
    return "chip subtle";
  }
  return "chip subtle";
}

function setRuntimeChip(message, tone = "neutral") {
  refs.runtimeChip.dataset.tone = tone;
  refs.runtimeChip.textContent = message;
}

function money(value, currency = "XAF") {
  if (value === null || value === undefined || value === "") {
    return "n/a";
  }
  const formatted = moneyFormatter.format(Number(value));
  return `${formatted} ${currency}`;
}

function propertyPrice(property) {
  if (property.price) {
    return {
      min: property.price.min,
      max: property.price.max,
      currency: property.price.currency || "XAF",
    };
  }
  return {
    min: property.price_min,
    max: property.price_max,
    currency: property.currency || "XAF",
  };
}

function propertyGeo(property) {
  if (property.geo) {
    return property.geo;
  }
  return {
    city: property.city,
    country: property.country,
    region: property.region,
    address_line: property.address_line,
    coordinates: { latitude: property.latitude, longitude: property.longitude },
  };
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
    const formatted = formatApiError(payload, response.status);
    const error = new Error(formatted.message);
    error.code = formatted.code;
    throw error;
  }

  return payload;
}

async function apiMultipart(path, { auth = false, formData }) {
  const response = await fetch(path, {
    method: "POST",
    headers: requestHeaders({}, auth),
    body: formData,
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
    const formatted = formatApiError(payload, response.status);
    const error = new Error(formatted.message);
    error.code = formatted.code;
    throw error;
  }
  return payload;
}

function clearNode(node) {
  node.replaceChildren();
}

function renderStat(label, value, accent = "") {
  const item = document.createElement("article");
  item.className = "stat-card";
  if (accent) {
    item.dataset.accent = accent;
  }
  const statLabel = document.createElement("span");
  statLabel.className = "stat-label";
  statLabel.textContent = label;
  const statValue = document.createElement("strong");
  statValue.textContent = value;
  item.append(statLabel, statValue);
  return item;
}

function renderSummary(summary) {
  const fragment = document.createDocumentFragment();
  const cards = [
    ["Organizations", summary.organizations ?? 0, "teal"],
    ["Users", summary.users ?? 0, "gold"],
    ["Published properties", summary.published_properties ?? 0, "violet"],
    ["Conversations", summary.conversations ?? 0, "coral"],
    ["Messages", summary.messages ?? 0, "sea"],
    ["Notifications", summary.notifications ?? 0, "gold"],
    ["Media", summary.media ?? 0, "slate"],
    ["Projects", summary.projects ?? 0, "teal"],
  ];
  cards.forEach(([label, value, accent]) => fragment.appendChild(renderStat(label, value, accent)));
  refs.statusStrip.replaceChildren(fragment);
}

function renderList(target, items, renderer, emptyText) {
  const fragment = document.createDocumentFragment();
  if (!items || !items.length) {
    const empty = document.createElement("p");
    empty.className = "muted empty-state";
    empty.textContent = emptyText;
    target.replaceChildren(empty);
    return;
  }
  items.forEach((item) => fragment.appendChild(renderer(item)));
  target.replaceChildren(fragment);
}

function renderOrganizations(items) {
  renderList(refs.organizationsList, items, (organization) => {
    const article = document.createElement("article");
    article.className = "mini-card";
    article.innerHTML = `
      <div class="mini-card__header">
        <strong>${escapeHtml(organization.name)}</strong>
        <span class="chip subtle">${escapeHtml(organization.kind)}</span>
      </div>
      <p class="muted">${escapeHtml(organization.slug)}</p>
      <p>${escapeHtml(organization.city || "No city")} · ${organization.user_count ?? 0} users</p>
    `;
    return article;
  }, "No organizations available.");

  const options = ['<option value="">None</option>']
    .concat(items.map((organization) => `<option value="${organization.id}">${escapeHtml(organization.name)}</option>`))
    .join("");
  refs.ownerOrganizationSelect.innerHTML = options;
  if (refs.registerOrganizationSelect) {
    refs.registerOrganizationSelect.innerHTML = options;
  }
  if (refs.adminOrganizationSelect) {
    refs.adminOrganizationSelect.innerHTML = ['<option value="">Select organization</option>']
      .concat(items.map((organization) => `<option value="${organization.id}">${escapeHtml(organization.name)}</option>`))
      .join("");
  }
}

function renderProjects(items) {
  if (!refs.projectsList) {
    return;
  }
  renderList(refs.projectsList, items, (project) => {
    const article = document.createElement("article");
    article.className = "mini-card mini-card--project";
    const budget = project.budget || {};
    article.innerHTML = `
      <div class="mini-card__header">
        <strong>${escapeHtml(project.title)}</strong>
        <span class="${statusChipClass(project.status)}">${escapeHtml(project.status)}</span>
      </div>
      <p class="muted">${escapeHtml(project.project_type)} · ${project.progress_percent ?? 0}% · ${escapeHtml(project.priority || "normal")}</p>
      <p>${escapeHtml(project.location?.city || "—")} · ${money(budget.min, budget.currency)} - ${money(budget.max, budget.currency)}</p>
      <p class="muted">${escapeHtml(project.objective || "")}</p>
    `;
    article.addEventListener("click", () => selectProject(project.id));
    return article;
  }, state.token ? "No projects yet — create one from the sidebar." : "Sign in to view projects.");
}

async function refreshEcosystemLists() {
  if (!state.token) {
    renderList(refs.partnersList, [], () => document.createElement("div"), "Sign in to load partners.");
    renderList(refs.servicesList, [], () => document.createElement("div"), "Sign in to load services.");
    return;
  }
  try {
    const [partnersPayload, servicesPayload] = await Promise.all([
      api("/api/v2/partners", { auth: true, query: { limit: 8 } }),
      api("/api/v2/services", { auth: true, query: { limit: 8 } }),
    ]);
    renderList(refs.partnersList, partnersPayload.partners || [], (partner) => {
      const article = document.createElement("article");
      article.className = "mini-card";
      article.innerHTML = `
        <strong>${escapeHtml(partner.display_name)}</strong>
        <p class="muted">${escapeHtml(partner.partner_type)} · Trust ${partner.trust_score ?? "n/a"}</p>
      `;
      return article;
    }, "No partners in directory.");
    renderList(refs.servicesList, servicesPayload.services || [], (service) => {
      const article = document.createElement("article");
      article.className = "mini-card";
      const pricing = service.pricing || {};
      article.innerHTML = `
        <strong>${escapeHtml(service.title)}</strong>
        <p class="muted">${escapeHtml(service.category)} · ${money(pricing.min, pricing.currency)} - ${money(pricing.max, pricing.currency)}</p>
      `;
      return article;
    }, "No services in catalog.");
  } catch (error) {
    renderList(refs.partnersList, [], () => document.createElement("div"), error.message);
  }
}

async function selectProject(projectId) {
  if (!state.token || !refs.projectDetail) {
    return;
  }
  state.selectedProjectId = projectId;
  try {
    const [payload, orchPayload, matchPayload, wfPayload, graphPayload, intelPayload, nbaPayload, risksPayload, oppPayload] = await Promise.all([
      api(`/api/v2/projects/${projectId}/workspace`, { auth: true }),
      api(`/api/v2/projects/${projectId}/orchestration`, { auth: true }),
      api(`/api/v2/matching?project_id=${projectId}`, { auth: true }),
      api(`/api/v2/projects/${projectId}/workflows`, { auth: true }),
      api("/api/v2/knowledge/graph", { auth: true, query: { project_id: projectId } }),
      api("/api/v2/intelligence", { auth: true, query: { project_id: projectId } }),
      api("/api/v2/next-actions", { auth: true, query: { project_id: projectId } }),
      api("/api/v2/risks", { auth: true, query: { project_id: projectId } }),
      api("/api/v2/opportunities", { auth: true, query: { project_id: projectId } }),
    ]);
    const workspace = payload.workspace || payload;
    const orchestration = orchPayload.orchestration || {};
    const matches = matchPayload.matches || [];
    const workflow = wfPayload.workflow_instance || {};
    const graph = graphPayload.graph || {};
    const cognitionIntel = intelPayload.intelligence || {};
    const nextAction = nbaPayload.next_action || {};
    const cognitionRisks = risksPayload.risks || [];
    const cognitionOpportunities = oppPayload.opportunities || [];
    const project = workspace.project;
    const progress = workspace.progress || {};
    const stepsHtml = (workspace.steps || [])
      .map(
        (step) => `
          <article class="message">
            <div class="message__meta">
              <strong>${escapeHtml(step.title)}</strong>
              <span class="chip subtle">${escapeHtml(step.status)}</span>
            </div>
            <p class="muted">${escapeHtml(step.milestone || "")} · ${escapeHtml(step.next_action || "")}</p>
          </article>
        `,
      )
      .join("");
    const goalsHtml = (workspace.goals || [])
      .slice(0, 5)
      .map((goal) => `<li>${escapeHtml(goal.title || goal.goal_key)} · ${escapeHtml(goal.status || "active")}</li>`)
      .join("");
    const timeline = workspace.timeline || {};
    const timelineHtml = (timeline.past_events || timeline.history || [])
      .slice(0, 4)
      .map((entry) => `<li>${escapeHtml(entry.title || entry.to_status || entry.kind || "Event")}</li>`)
      .join("");
    const tasksHtml = (workspace.tasks || [])
      .slice(0, 5)
      .map((task) => `<li>${escapeHtml(task.title)} · ${escapeHtml(task.status || "pending")}</li>`)
      .join("");
    const lifeEventsHtml = (workspace.life_events || [])
      .slice(0, 4)
      .map((event) => `<li>${escapeHtml(event.title || event.event_type)}</li>`)
      .join("");
    const graphNodesHtml = (graph.nodes || [])
      .slice(0, 6)
      .map((node) => `<li>${escapeHtml(node.title || node.node_key)} · ${escapeHtml(node.node_type || "")}</li>`)
      .join("");
    const cognitionRisksHtml = cognitionRisks
      .slice(0, 4)
      .map((risk) => `<li>${escapeHtml(risk.risk_key || "risk")} · score ${risk.score ?? "n/a"}</li>`)
      .join("");
    const cognitionOpportunitiesHtml = cognitionOpportunities
      .slice(0, 4)
      .map((item) => `<li>${escapeHtml(item.opportunity_key || "opportunity")} · ${item.opportunity_score ?? "n/a"}</li>`)
      .join("");
    const knowledgeHtml = (workspace.knowledge || [])
      .slice(0, 4)
      .map((fact) => `<li>${escapeHtml(fact.title)} · ${escapeHtml(fact.category || "")}</li>`)
      .join("");
    const actionsListHtml = (workspace.actions || [])
      .slice(0, 4)
      .map((action) => `<li>${escapeHtml(action.title)} · ${escapeHtml(action.status || "pending")}</li>`)
      .join("");
    const recommendationsHtml = (workspace.recommendations || workspace.next_actions || [])
      .slice(0, 3)
      .map((action) => `<li>${escapeHtml(action.title || action.next_action || "Action")}</li>`)
      .join("");
    const partnerMatchesHtml = matches
      .filter((m) => m.match_type === "partner" || m.partner)
      .slice(0, 4)
      .map((m) => {
        const label = m.partner?.display_name || m.partner_type || "Partner";
        return `<li>${escapeHtml(label)} · score ${m.score} · ${escapeHtml((m.rationale?.[0]?.label) || "")}</li>`;
      })
      .join("");
    const serviceMatchesHtml = matches
      .filter((m) => m.match_type === "service" || m.service)
      .slice(0, 4)
      .map((m) => {
        const label = m.service?.title || m.service_key || "Service";
        return `<li>${escapeHtml(label)} · score ${m.score}</li>`;
      })
      .join("");
    const interventionsHtml = (orchestration.planning || [])
      .slice(0, 4)
      .map((item) => `<li>${escapeHtml(item.title || item.type)} · ${escapeHtml(item.status || "")}</li>`)
      .join("");
    refs.projectDetail.innerHTML = `
      <div class="detail-summary">
        <div>
          <p class="eyebrow">${escapeHtml(project.project_type)} project</p>
          <h3>${escapeHtml(project.title)}</h3>
          <p>${escapeHtml(project.objective)}</p>
          <p class="muted">Progress ${progress.progress_percent ?? 0}% · ${progress.steps_completed ?? 0}/${progress.steps_total ?? 0} steps · Journey ${escapeHtml(workspace.journey?.status || workspace.journey_state?.status || "active")}</p>
        </div>
      </div>
      <div class="detail-grid">
        <section>
          <h4>Ecosystem — partner matches</h4>
          <ul>${partnerMatchesHtml || "<li class='muted'>No partner matches</li>"}</ul>
        </section>
        <section>
          <h4>Ecosystem — service matches</h4>
          <ul>${serviceMatchesHtml || "<li class='muted'>No service matches</li>"}</ul>
        </section>
        <section>
          <h4>Workflow</h4>
          <p class="muted">${escapeHtml(workflow.status || "—")} · ${workflow.progress_percent ?? 0}% · step ${escapeHtml(workflow.current_step_key || "—")}</p>
        </section>
        <section>
          <h4>Interventions</h4>
          <ul>${interventionsHtml || "<li class='muted'>No interventions planned</li>"}</ul>
        </section>
        <section>
          <h4>Orchestration</h4>
          <p class="muted">${orchestration.partners_engaged ?? 0} partners · ${orchestration.services_recommended ?? 0} services · ${money(orchestration.cost_summary?.estimated, orchestration.cost_summary?.currency)} estimated</p>
        </section>
        <section>
          <h4>Goals</h4>
          <ul>${goalsHtml || "<li class='muted'>No goals</li>"}</ul>
        </section>
        <section>
          <h4>Recommendations</h4>
          <ul>${recommendationsHtml || "<li class='muted'>No recommendations</li>"}</ul>
        </section>
        <section>
          <h4>Intelligence</h4>
          <p class="muted">Blockers: ${workspace.intelligence?.blockers?.open_high_risks ?? 0} high risks · Trust ${workspace.trust_score?.score ?? "n/a"}</p>
          <p class="muted">Priorities: ${escapeHtml((workspace.intelligence?.priorities || []).slice(0, 2).join(" · ") || "—")}</p>
        </section>
        <section>
          <h4>Timeline</h4>
          <ul>${timelineHtml || "<li class='muted'>No timeline entries</li>"}</ul>
        </section>
        <section>
          <h4>Actions</h4>
          <ul>${actionsListHtml || "<li class='muted'>No actions</li>"}</ul>
        </section>
        <section>
          <h4>Tasks</h4>
          <ul>${tasksHtml || "<li class='muted'>No tasks</li>"}</ul>
        </section>
        <section>
          <h4>Life events</h4>
          <ul>${lifeEventsHtml || "<li class='muted'>No life events</li>"}</ul>
        </section>
        <section>
          <h4>Knowledge graph</h4>
          <p class="muted">${(graph.nodes || []).length} nodes · ${(graph.edges || []).length} edges</p>
          <ul>${graphNodesHtml || "<li class='muted'>No graph nodes</li>"}</ul>
        </section>
        <section>
          <h4>Decision platform</h4>
          <p class="muted">${escapeHtml(nextAction.title || "—")} · confidence ${nextAction.confidence ?? "n/a"}</p>
          <p class="muted">${escapeHtml(nextAction.justification || cognitionIntel.snapshot?.decision?.reason || "—")}</p>
        </section>
        <section>
          <h4>Next best action</h4>
          <p class="muted">${escapeHtml(nextAction.title || "—")} · score ${nextAction.score ?? "n/a"}</p>
        </section>
        <section>
          <h4>Risk intelligence</h4>
          <ul>${cognitionRisksHtml || "<li class='muted'>No risk scores</li>"}</ul>
        </section>
        <section>
          <h4>Opportunity intelligence</h4>
          <ul>${cognitionOpportunitiesHtml || "<li class='muted'>No opportunities scored</li>"}</ul>
        </section>
        <section>
          <h4>Knowledge</h4>
          <ul>${knowledgeHtml || "<li class='muted'>No knowledge facts</li>"}</ul>
        </section>
      </div>
      <h4>Journey steps</h4>
      <div class="message-stream">${stepsHtml}</div>
    `;
  } catch (error) {
    refs.projectDetail.innerHTML = `<p class="muted">${escapeHtml(error.message)}</p>`;
  }
}

async function refreshProjects() {
  if (!state.token || !refs.projectsList) {
    renderProjects([]);
    return;
  }
  try {
    const payload = await api("/api/v2/projects", { auth: true, query: { limit: 20 } });
    renderProjects(payload.projects || []);
    if (state.selectedProjectId) {
      await selectProject(state.selectedProjectId);
    }
  } catch (error) {
    renderProjects([]);
  }
}

function renderProperties(items) {
  const mediaOptions = ['<option value="">Select property</option>']
    .concat(
      (items || []).map((property) => {
        const label = property.listing_code || property.title;
        return `<option value="${property.id}">${escapeHtml(label)}</option>`;
      }),
    )
    .join("");
  refs.mediaPropertySelect.innerHTML = mediaOptions;

  renderList(refs.propertiesList, items, (property) => {
    const price = propertyPrice(property);
    const geo = propertyGeo(property);
    const coords = geo.coordinates || {};
    const article = document.createElement("article");
    article.className = "mini-card mini-card--property";
    article.innerHTML = `
      <div class="mini-card__header">
        <strong>${escapeHtml(property.title)}</strong>
        <span class="${statusChipClass(property.status)}" data-status="${escapeHtml(property.status || "draft")}">${escapeHtml(property.status || "draft")}</span>
      </div>
      <p class="muted">${escapeHtml(property.listing_code || "no-code")} · ${escapeHtml(property.property_type || "n/a")} · ${escapeHtml(property.availability || "available")}</p>
      <p>${escapeHtml(geo.city || "n/a")}, ${escapeHtml(geo.region || "—")}, ${escapeHtml(geo.country || "n/a")}</p>
      <p>${money(price.min, price.currency)} - ${money(price.max, price.currency)}</p>
      <p class="muted">Coords: ${coords.latitude ?? "—"}, ${coords.longitude ?? "—"}</p>
      <p class="muted">Owner: ${escapeHtml(property.ownership?.organization_name || property.owner_organization_name || "n/a")} · Media: ${property.media_count ?? 0}</p>
      <p>${escapeHtml(property.summary || "")}</p>
    `;
    article.addEventListener("click", () => {
      state.selectedPropertyId = property.id;
      state.selectedPropertyVersion = property.version;
      state.selectedPropertyTitle = property.title;
      updateSelectedPropertyLabel();
      setNotice(`Selected property #${property.id} (${property.title})`, "neutral");
    });
    return article;
  }, "No properties available.");
}

function renderMedia(items) {
  renderList(refs.mediaList, items, (media) => {
    const article = document.createElement("article");
    article.className = "mini-card mini-card--media";
    const preview =
      media.mime_type?.startsWith("image/") && media.url
        ? `<img class="media-preview" src="${escapeHtml(media.url)}" alt="${escapeHtml(media.caption || media.kind)}" loading="lazy">`
        : "";
    article.innerHTML = `
      ${preview}
      <div class="mini-card__header">
        <strong>${escapeHtml(media.caption || media.kind)}</strong>
        <span class="chip subtle">${escapeHtml(media.kind)}</span>
      </div>
      <p class="muted">${escapeHtml(media.property_title || `Property #${media.property_id}`)}</p>
      <p>${escapeHtml(media.mime_type || "unknown")} · ${media.size_bytes ?? 0} bytes</p>
      <p class="muted">${escapeHtml(media.url)}</p>
    `;
    return article;
  }, "No media available.");
}

function renderMatches(items) {
  renderList(refs.matchesList, items, (match) => {
    const property = match.property;
    const price = propertyPrice(property);
    const geo = propertyGeo(property);
    const breakdown = match.breakdown || {};
    const breakdownText = Object.entries(breakdown)
      .map(([key, value]) => `${key}:${value}`)
      .join(" · ");
    const article = document.createElement("article");
    article.className = "mini-card mini-card--match";
    article.innerHTML = `
      <div class="mini-card__header">
        <strong>${escapeHtml(property.title)}</strong>
        <span class="chip accent">${match.score} · ${escapeHtml(match.grade || "n/a")}</span>
      </div>
      <p class="muted">${escapeHtml(geo.city || property.city)}, ${escapeHtml(geo.country || property.country)}</p>
      <p>${money(price.min, price.currency)} - ${money(price.max, price.currency)}</p>
      <p class="muted">${escapeHtml(match.summary || (match.reasons || []).join(" · ") || "No summary.")}</p>
      <p class="muted breakdown">${escapeHtml(breakdownText || "No score breakdown.")}</p>
    `;
    return article;
  }, "No match results yet.");
}

function conversationRequester(conversation) {
  return conversation.requester?.full_name || conversation.requester_name || "n/a";
}

function conversationPropertyTitle(conversation) {
  return conversation.property?.title || conversation.property_title || "n/a";
}

function messageSenderName(message) {
  return message.sender?.full_name || message.sender_name || "n/a";
}

function renderConversationDetail(conversation) {
  const messages = conversation.messages || [];
  const negotiation = conversation.negotiation || {};
  const allowedStages = negotiation.allowed_stages || [];
  refs.conversationDetail.innerHTML = `
    <div class="detail-summary">
      <div>
        <p class="eyebrow">
          <span class="chip subtle" data-status="${escapeHtml(conversation.status)}">${escapeHtml(conversation.status)}</span>
          <span class="chip accent">${escapeHtml(conversation.negotiation_stage || negotiation.stage || "inquiry")}</span>
        </p>
        <h3>${escapeHtml(conversation.subject)}</h3>
        <p class="muted">
          Requester: ${escapeHtml(conversationRequester(conversation))} · Property: ${escapeHtml(conversationPropertyTitle(conversation))}
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
                <strong>${escapeHtml(messageSenderName(message))}</strong>
                <span class="muted">${escapeHtml(message.created_at)}</span>
              </div>
              <p>${escapeHtml(message.body)}</p>
            </article>
          `,
        )
        .join("")}
    </div>
  `;
  refs.messageForm.classList.toggle("hidden", !state.token);
  if (refs.negotiationForm) {
    const stageSelect = refs.negotiationForm.querySelector('[name="negotiation_stage"]');
    if (stageSelect) {
      stageSelect.innerHTML = allowedStages
        .map((stage) => `<option value="${stage}" ${stage === (conversation.negotiation_stage || "inquiry") ? "selected" : ""}>${stage}</option>`)
        .join("");
    }
    refs.negotiationForm.classList.toggle("hidden", !state.token || !allowedStages.length);
  }
}

function renderNotifications(items) {
  const unread = (items || []).filter((notification) => !notification.read).length;
  if (refs.notificationUnreadCount) {
    refs.notificationUnreadCount.textContent = `${unread} unread`;
    refs.notificationUnreadCount.dataset.tone = unread ? "warn" : "ok";
  }
  renderList(refs.notificationsList, items, (notification) => {
    const article = document.createElement("article");
    article.className = "mini-card mini-card--notification";
    if (!notification.read) {
      article.dataset.unread = "true";
    }
    article.innerHTML = `
      <div class="mini-card__header">
        <strong>${escapeHtml(notification.title)}</strong>
        <span class="chip subtle">${escapeHtml(notification.kind)}</span>
      </div>
      <p>${escapeHtml(notification.body)}</p>
      <p class="muted">${notification.read ? "read" : "unread"} · ${escapeHtml(notification.created_at || "")}</p>
    `;
    article.addEventListener("click", () => markNotificationRead(notification.id));
    return article;
  }, "No notifications yet.");
}

async function refreshNotifications() {
  if (!state.token) {
    renderNotifications([]);
    return;
  }
  const form = refs.notificationFilterForm ? new FormData(refs.notificationFilterForm) : null;
  const payload = await api("/api/notifications", {
    auth: true,
    query: {
      limit: 20,
      kind: form?.get("kind") || undefined,
      unread_only: form?.get("unread_only") ? "true" : undefined,
    },
  });
  renderNotifications(payload.notifications || []);
}

async function markNotificationRead(notificationId) {
  if (!state.token) {
    return;
  }
  try {
    await api(`/api/notifications/${notificationId}/read`, { method: "PATCH", auth: true, body: {} });
    await refreshNotifications();
  } catch (error) {
    setNotice(error.message, "error");
  }
}

async function markAllNotificationsRead() {
  if (!state.token) {
    return;
  }
  try {
    await api("/api/notifications/read-all", { method: "POST", auth: true, body: {} });
    await refreshNotifications();
    setNotice("All notifications marked as read.", "ok");
  } catch (error) {
    setNotice(error.message, "error");
  }
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
        <strong>${escapeHtml(conversation.subject)}</strong>
        <span class="chip subtle">${escapeHtml(conversation.status)} · ${escapeHtml(conversation.negotiation_stage || "inquiry")}</span>
      </div>
      <p class="muted">${escapeHtml(conversationRequester(conversation))} · ${escapeHtml(conversationPropertyTitle(conversation))}</p>
      <p>${escapeHtml(conversation.last_message || "No messages yet.")}</p>
    `;
    article.addEventListener("click", () => selectConversation(conversation.id));
    return article;
  }, "No conversations available.");
}

function updateSelectedPropertyLabel() {
  if (!refs.selectedPropertyLabel) {
    return;
  }
  if (!state.selectedPropertyId) {
    refs.selectedPropertyLabel.textContent = "No property selected.";
    return;
  }
  refs.selectedPropertyLabel.textContent = `#${state.selectedPropertyId} · ${state.selectedPropertyTitle || "Property"} · v${state.selectedPropertyVersion ?? "?"}`;
}

function applyJourney(journey) {
  state.activeJourney = journey;
  localStorage.setItem("lawim.journey", journey);
  document.querySelectorAll("[data-journey-panel]").forEach((panel) => {
    const allowed = (panel.getAttribute("data-journey-panel") || "").split(/\s+/);
    panel.hidden = !allowed.includes(journey);
  });
  document.querySelectorAll("#journey-nav [data-journey]").forEach((button) => {
    button.dataset.active = button.getAttribute("data-journey") === journey ? "true" : "false";
  });
  if (journey === "admin" && state.token) {
    loadAdminDashboard();
  }
}

async function loadAdminDashboard() {
  if (!refs.adminDashboard || !state.token) {
    return;
  }
  try {
    const [metrics, events] = await Promise.all([
      api("/api/metrics", { auth: true }),
      api("/api/events?limit=10", { auth: true }),
    ]);
    const counters = metrics.metrics || {};
    refs.adminDashboard.innerHTML = `
      <div class="detail-summary">
        <div>
          <p class="eyebrow">Runtime metrics</p>
          <p>Requests ${counters.requests_total ?? 0} · Matches ${counters.matches_total ?? 0} · Conversations ${counters.conversations_total ?? 0}</p>
        </div>
      </div>
      <div class="message-stream">
        ${(events.events || [])
          .map(
            (event) => `
              <article class="message">
                <div class="message__meta">
                  <strong>${escapeHtml(event.kind)}</strong>
                  <span class="muted">${escapeHtml(event.created_at)}</span>
                </div>
              </article>
            `,
          )
          .join("")}
      </div>
    `;
  } catch (error) {
    refs.adminDashboard.innerHTML = `<p class="muted">${escapeHtml(error.message)}</p>`;
  }
}

function renderHealth(health) {
  const environment = health.environment || {};
  const database = health.database || {};
  setRuntimeChip(`${health.status.toUpperCase()} · ${environment.app_env || "unknown"}`, health.status === "ok" ? "ok" : "warn");
  const metricsNote = health.metrics ? `${health.metrics.requests_total ?? 0} requests` : "metrics admin-only";
  refs.bootstrapSummary.textContent = `Driver ${environment.db_driver || database.driver || "sqlite"} · schema v${database.schema_version ?? "?"} · ${health.summary?.events ?? 0} events · ${metricsNote}.`;
}

function renderBootstrap(payload) {
  state.bootstrap = payload;
  maybePopulateDemoCredentials();
  if (refs.demoButton) {
    refs.demoButton.hidden = !payload.features?.demo_credentials;
  }
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
  renderMedia(payload.media || []);
  renderMatches(payload.matches || []);
  renderConversations(payload.conversations || []);
  renderNotifications(payload.notifications || []);

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
  try {
    const payload = await api(`/api/conversations/${conversationId}`, { auth: true });
    renderConversationDetail(payload.conversation);
    renderConversations(state.bootstrap?.conversations || []);
  } catch (error) {
    state.selectedConversationId = null;
    refs.conversationDetail.innerHTML = `<p class="muted">${error.message}</p>`;
    setNotice(error.message, "error", error.code || "");
  }
}

function parseNumber(value) {
  if (value === "" || value === null || value === undefined) {
    return null;
  }
  const parsed = Number(value);
  return Number.isFinite(parsed) ? parsed : null;
}

async function refresh() {
  if (state.refreshInFlight) {
    return;
  }
  state.refreshInFlight = true;
  setLoading(true, "Refreshing runtime state...");
  try {
    const healthPromise = api("/api/health", { auth: Boolean(state.token) });
    const bootstrapPromise = api("/api/bootstrap", { auth: Boolean(state.token) });
    const [health, bootstrap] = await Promise.all([healthPromise, bootstrapPromise]);
    state.health = health;
    renderHealth(health);
    renderBootstrap(bootstrap);
    await refreshProjects();
    await refreshEcosystemLists();
    applyJourney(state.activeJourney);
    setNotice("Runtime is available and ready.", "success");
  } catch (error) {
    setNotice(`${error.message} — retry with refresh or check ./scripts/run-local.sh`, "error", error.code || "");
    setRuntimeChip("DEGRADED", "warn");
  } finally {
    state.refreshInFlight = false;
    setLoading(false);
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

async function handleProjectCreate(event) {
  event.preventDefault();
  if (!state.token) {
    setNotice("Sign in to create a project.", "error");
    return;
  }
  try {
    const form = new FormData(refs.projectForm);
    const payload = await api("/api/v2/projects", {
      method: "POST",
      auth: true,
      body: {
        title: form.get("title"),
        objective: form.get("objective"),
        project_type: form.get("project_type"),
        budget_min: parseNumber(form.get("budget_min")),
        budget_max: parseNumber(form.get("budget_max")),
        location_city: form.get("location_city"),
        timeline_horizon: form.get("timeline_horizon"),
        status: "active",
      },
    });
    refs.projectForm.reset();
    state.selectedProjectId = payload.project.id;
    setNotice("Project created.", "success");
    await refreshProjects();
    applyJourney("project");
  } catch (error) {
    setNotice(error.message, "error", error.code || "");
  }
}

async function handleMatchSearch(event) {
  event.preventDefault();
  try {
    const form = new FormData(refs.matchForm);
    const payload = await api("/api/matches", {
      auth: Boolean(state.token),
      query: {
        city: form.get("city"),
        budget_min: parseNumber(form.get("budget_min")),
        budget_max: parseNumber(form.get("budget_max")),
        latitude: parseNumber(form.get("latitude")),
        longitude: parseNumber(form.get("longitude")),
        limit: parseNumber(form.get("limit")),
        min_score: parseNumber(form.get("min_score")),
      },
    });
    renderMatches(payload.matches || []);
    setNotice(`Returned ${payload.matches?.length || 0} ranked matches (min score ${payload.criteria?.min_score ?? "n/a"}).`, "success");
    if (state.token) {
      await refreshNotifications();
    }
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
        country: form.get("country") || "Cameroon",
        address_line: form.get("address_line"),
        region: form.get("region"),
        property_type: form.get("property_type"),
        status: form.get("status") || "draft",
        availability: form.get("availability") || "available",
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

async function handleGeoLookup(event) {
  event.preventDefault();
  try {
    const form = new FormData(refs.geoForm);
    const payload = await api("/api/geo/geocode", {
      query: {
        city: form.get("city"),
        country: form.get("country"),
        address_line: form.get("address_line"),
        region: form.get("region"),
      },
    });
    const location = payload.location || {};
    const coords = location.coordinates || {};
    refs.geoResult.textContent = `${location.city}, ${location.region || "—"}, ${location.country} · ${coords.latitude}, ${coords.longitude} · provider=${payload.provider}`;
    setNotice("Geo lookup completed.", "success");
  } catch (error) {
    refs.geoResult.textContent = error.message;
    setNotice(error.message, "error");
  }
}

async function handleMediaUpload(event) {
  event.preventDefault();
  if (!state.token) {
    setNotice("Authenticate before uploading media.", "error");
    return;
  }
  try {
    const form = new FormData(refs.mediaUploadForm);
    const file = form.get("file");
    const propertyId = form.get("property_id");
    if (!file || !propertyId) {
      throw new Error("Property and file are required.");
    }
    const uploadData = new FormData();
    uploadData.append("property_id", String(propertyId));
    uploadData.append("file", file);
    uploadData.append("caption", form.get("caption") || "Uploaded media");
    uploadData.append("kind", form.get("kind") || "image");
    await apiMultipart("/api/media/upload", { auth: true, formData: uploadData });
    refs.mediaUploadForm.reset();
    setNotice("Media uploaded.", "success");
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

function maybePopulateDemoCredentials() {
  if (state.bootstrap?.features?.demo_credentials) {
    populateDemoCredentials();
  }
}

function populateDemoCredentials() {
  refs.loginEmail.value = "admin@lawim.local";
  refs.loginPassword.value = "lawim-demo";
}

async function handleRegister(event) {
  event.preventDefault();
  try {
    const form = new FormData(refs.registerForm);
    const payload = await api("/api/auth/register", {
      method: "POST",
      body: {
        full_name: form.get("full_name"),
        email: form.get("email"),
        password: form.get("password"),
        role: form.get("role"),
        organization_id: parseNumber(form.get("organization_id")),
      },
    });
    state.token = payload.token;
    localStorage.setItem("lawim.token", state.token);
    applyJourney(form.get("role") === "agent" ? "seller" : "buyer");
    setNotice(`Registered as ${payload.user.email}`, "success");
    await refresh();
  } catch (error) {
    setNotice(error.message, "error");
  }
}

async function handlePropertySearch(event) {
  event.preventDefault();
  try {
    const form = new FormData(refs.propertySearchForm);
    const payload = await api("/api/properties", {
      query: {
        city: form.get("city"),
        region: form.get("region"),
        property_type: form.get("property_type"),
        status: form.get("status"),
        price_min: parseNumber(form.get("price_min")),
        price_max: parseNumber(form.get("price_max")),
        sort: form.get("sort") || "created_at",
        order: form.get("order") || "desc",
        page: parseNumber(form.get("page")) || 1,
        limit: parseNumber(form.get("limit")) || 10,
      },
    });
    renderProperties(payload.properties || []);
    const pagination = payload.pagination || {};
    if (refs.propertySearchMeta) {
      refs.propertySearchMeta.textContent = `Page ${pagination.page || 1}/${pagination.pages || 1} · ${pagination.total ?? payload.properties?.length ?? 0} total · sort ${pagination.sort || "created_at"} ${pagination.order || "desc"}`;
    }
    setNotice(`Found ${payload.properties?.length || 0} listings.`, "success");
  } catch (error) {
    setNotice(error.message, "error", error.code || "");
  }
}

async function handlePublishProperty() {
  if (!state.token || !state.selectedPropertyId) {
    setNotice("Select a property and authenticate first.", "error");
    return;
  }
  try {
    const payload = await api(`/api/properties/${state.selectedPropertyId}/publish`, {
      method: "POST",
      auth: true,
      body: { version: state.selectedPropertyVersion },
    });
    state.selectedPropertyVersion = payload.property.version;
    updateSelectedPropertyLabel();
    setNotice("Property published.", "success");
    await refresh();
  } catch (error) {
    setNotice(error.message, "error");
  }
}

async function handleArchiveProperty() {
  if (!state.token || !state.selectedPropertyId) {
    setNotice("Select a property and authenticate first.", "error");
    return;
  }
  try {
    const payload = await api(`/api/properties/${state.selectedPropertyId}`, {
      method: "PATCH",
      auth: true,
      body: { status: "archived", version: state.selectedPropertyVersion },
    });
    state.selectedPropertyVersion = payload.property.version;
    updateSelectedPropertyLabel();
    setNotice("Property archived.", "success");
    await refresh();
  } catch (error) {
    setNotice(error.message, "error");
  }
}

async function handleBuyerConversation(event) {
  event.preventDefault();
  if (!state.token || !state.selectedPropertyId) {
    setNotice("Select a property and authenticate first.", "error");
    return;
  }
  try {
    const form = new FormData(refs.buyerConversationForm);
    const payload = await api("/api/conversations", {
      method: "POST",
      auth: true,
      body: {
        property_id: state.selectedPropertyId,
        subject: form.get("subject"),
        initial_message: form.get("initial_message"),
      },
    });
    refs.buyerConversationForm.reset();
    state.selectedConversationId = payload.conversation.id;
    setNotice("Conversation opened.", "success");
    await refresh();
    await selectConversation(payload.conversation.id);
  } catch (error) {
    setNotice(error.message, "error", error.code || "");
  }
}

async function handleNegotiationUpdate(event) {
  event.preventDefault();
  if (!state.token || !state.selectedConversationId) {
    setNotice("Select a conversation first.", "error");
    return;
  }
  try {
    const form = new FormData(refs.negotiationForm);
    const payload = await api(`/api/conversations/${state.selectedConversationId}`, {
      method: "PATCH",
      auth: true,
      body: { negotiation_stage: form.get("negotiation_stage") },
    });
    renderConversationDetail(payload.conversation);
    setNotice(`Negotiation stage updated to ${payload.conversation.negotiation_stage}.`, "success");
    await refresh();
    await refreshNotifications();
  } catch (error) {
    setNotice(error.message, "error", error.code || "");
  }
}

async function handleNotificationFilter(event) {
  event.preventDefault();
  try {
    await refreshNotifications();
    setNotice("Notification filter applied.", "success");
  } catch (error) {
    setNotice(error.message, "error", error.code || "");
  }
}

async function handleAdminOrgCreate(event) {
  event.preventDefault();
  if (!state.token) {
    setNotice("Authenticate as admin first.", "error");
    return;
  }
  try {
    const form = new FormData(refs.adminOrgForm);
    await api("/api/organizations", {
      method: "POST",
      auth: true,
      body: { name: form.get("name"), slug: form.get("slug"), kind: "agency", city: "Douala" },
    });
    refs.adminOrgForm.reset();
    setNotice("Organization created.", "success");
    await refresh();
  } catch (error) {
    setNotice(error.message, "error");
  }
}

async function handleAdminUserCreate(event) {
  event.preventDefault();
  if (!state.token) {
    setNotice("Authenticate as admin first.", "error");
    return;
  }
  try {
    const form = new FormData(refs.adminUserForm);
    await api("/api/users", {
      method: "POST",
      auth: true,
      body: {
        email: form.get("email"),
        full_name: form.get("full_name"),
        role: "agent",
        password: form.get("password") || "lawim-demo",
        organization_id: parseNumber(form.get("organization_id")),
      },
    });
    refs.adminUserForm.reset();
    setNotice("Staff user created.", "success");
    await refresh();
  } catch (error) {
    setNotice(error.message, "error");
  }
}

function bindEvents() {
  refs.loginForm.addEventListener("submit", handleLogin);
  refs.logoutButton.addEventListener("click", handleLogout);
  refs.demoButton.addEventListener("click", populateDemoCredentials);
  refs.registerForm?.addEventListener("submit", handleRegister);
  refs.projectForm?.addEventListener("submit", handleProjectCreate);
  refs.propertySearchForm?.addEventListener("submit", handlePropertySearch);
  refs.matchForm.addEventListener("submit", handleMatchSearch);
  refs.propertyForm.addEventListener("submit", handlePropertyCreate);
  refs.geoForm.addEventListener("submit", handleGeoLookup);
  refs.mediaUploadForm.addEventListener("submit", handleMediaUpload);
  refs.messageForm.addEventListener("submit", handleMessageCreate);
  refs.buyerConversationForm?.addEventListener("submit", handleBuyerConversation);
  refs.negotiationForm?.addEventListener("submit", handleNegotiationUpdate);
  refs.notificationFilterForm?.addEventListener("submit", handleNotificationFilter);
  refs.adminOrgForm?.addEventListener("submit", handleAdminOrgCreate);
  refs.adminUserForm?.addEventListener("submit", handleAdminUserCreate);
  refs.publishPropertyButton?.addEventListener("click", handlePublishProperty);
  refs.archivePropertyButton?.addEventListener("click", handleArchiveProperty);
  refs.journeyNav?.querySelectorAll("[data-journey]").forEach((button) => {
    button.addEventListener("click", () => applyJourney(button.getAttribute("data-journey")));
  });
  if (refs.markNotificationsReadButton) {
    refs.markNotificationsReadButton.addEventListener("click", markAllNotificationsRead);
  }
}

document.addEventListener("DOMContentLoaded", async () => {
  cacheRefs();
  bindEvents();
  applyJourney(state.activeJourney);
  updateSelectedPropertyLabel();
  await refresh();
});
