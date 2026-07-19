const avatarConfig = {
  avatarAssetUrl:
    "https://raw.githubusercontent.com/<owner>/<repo>/<branch>/artifacts/exports/avatars/avatar.gif",
  fallbackMessage:
    "Replace the template URL with the public GIF URL from Colab.",
  privateUrlMessage:
    "Use a public HTTPS GIF URL from Colab; private or local URLs will not load.",
};

function hasTemplatePlaceholder(value) {
  return /<[^>]+>/.test(value);
}

function getAvatarAssetUrlState(value) {
  if (typeof value !== "string") {
    return {
      isConfigured: false,
      isPublicHttps: false,
      message: avatarConfig.privateUrlMessage,
    };
  }

  const trimmed = value.trim();

  if (!trimmed) {
    return {
      isConfigured: false,
      isPublicHttps: false,
      message: avatarConfig.privateUrlMessage,
    };
  }

  if (hasTemplatePlaceholder(trimmed)) {
    return {
      isConfigured: false,
      isPublicHttps: false,
      message: avatarConfig.fallbackMessage,
    };
  }

  if (!/^https:\/\/[^\s]+$/i.test(trimmed)) {
    return {
      isConfigured: false,
      isPublicHttps: false,
      message: avatarConfig.privateUrlMessage,
    };
  }

  if (/^https:\/\/(localhost|127\.|0\.0\.0\.0)(:\d+)?/i.test(trimmed)) {
    return {
      isConfigured: false,
      isPublicHttps: false,
      message: avatarConfig.privateUrlMessage,
    };
  }

  return {
    isConfigured: true,
    isPublicHttps: true,
    message: "Connected to a public avatar URL.",
  };
}

function isPublicHttpsUrl(value) {
  return getAvatarAssetUrlState(value).isPublicHttps;
}

function setStatus(element, message, tone) {
  if (!element) {
    return;
  }

  element.textContent = message;
  element.dataset.tone = tone;
}

function renderAvatar() {
  const preview = document.getElementById("avatarPreview");
  const status = document.getElementById("assetStatus");
  const url = avatarConfig.avatarAssetUrl;
  const assetUrlState = getAvatarAssetUrlState(url);

  if (!preview) {
    return;
  }

  if (assetUrlState.isPublicHttps) {
    preview.src = url.trim();
    preview.classList.remove("is-fallback");
    setStatus(status, assetUrlState.message, "success");
    return;
  }

  preview.removeAttribute("src");
  preview.classList.add("is-fallback");
  setStatus(status, assetUrlState.message, "warning");
}

function wireBadgeControls() {
  const badge = document.getElementById("previewBadge");
  const input = document.getElementById("badgeInput");
  const toggle = document.getElementById("badgeToggle");

  if (input && badge) {
    input.addEventListener("input", () => {
      badge.textContent = input.value.trim() || "Workshop badge";
    });
  }

  if (toggle && badge) {
    toggle.addEventListener("click", () => {
      const isHidden = badge.hidden;
      badge.hidden = !isHidden;
      toggle.textContent = isHidden ? "Hide badge" : "Show badge";
    });
  }
}

function validateWorkshopConfig() {
  const assetUrlState = getAvatarAssetUrlState(avatarConfig.avatarAssetUrl);

  return {
    avatarAssetUrl: avatarConfig.avatarAssetUrl,
    avatarAssetUrlIsConfigured: assetUrlState.isConfigured,
    avatarAssetUrlIsPublicHttps: assetUrlState.isPublicHttps,
    avatarAssetUrlStatusMessage: assetUrlState.message,
  };
}

document.addEventListener("DOMContentLoaded", () => {
  renderAvatar();
  wireBadgeControls();
});

window.avatarConfig = avatarConfig;
window.avatarWorkshopValidate = validateWorkshopConfig;
