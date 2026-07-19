const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');

const SCRIPT_PATH = path.join(__dirname, 'script.js');
const SCRIPT_SOURCE = fs.readFileSync(SCRIPT_PATH, 'utf8');

function assert(condition, message) {
  if (!condition) {
    throw new Error(message);
  }
}

function createContext() {
  const context = {
    console,
    document: {
      addEventListener() {},
      getElementById() {
        return null;
      },
    },
  };

  context.window = context;
  context.globalThis = context;

  return vm.createContext(context);
}

function loadStarter() {
  new vm.Script(SCRIPT_SOURCE, { filename: SCRIPT_PATH });

  const context = createContext();
  new vm.Script(SCRIPT_SOURCE, { filename: SCRIPT_PATH }).runInContext(context);

  assert(
    typeof context.avatarWorkshopValidate === 'function',
    'Expected avatarWorkshopValidate to be defined.'
  );

  assert(
    context.avatarConfig && typeof context.avatarConfig === 'object',
    'Expected avatarConfig to be defined.'
  );

  return context;
}

function runValidation() {
  const context = loadStarter();

  const placeholderState = context.avatarWorkshopValidate();
  assert(
    placeholderState.avatarAssetUrlIsConfigured === false,
    'Template placeholder URL should be treated as unconfigured.'
  );
  assert(
    placeholderState.avatarAssetUrlIsPublicHttps === false,
    'Template placeholder URL should fail the public HTTPS check.'
  );
  assert(
    placeholderState.avatarAssetUrlStatusMessage ===
      'Replace the template URL with the public GIF URL from Colab.',
    'Template placeholder URL should produce fallback guidance.'
  );

  context.avatarConfig.avatarAssetUrl = 'http://example.com/avatar.gif';
  const insecureState = context.avatarWorkshopValidate();
  assert(
    insecureState.avatarAssetUrlIsConfigured === false,
    'Non-HTTPS URLs should not be treated as configured.'
  );
  assert(
    insecureState.avatarAssetUrlIsPublicHttps === false,
    'Non-HTTPS URLs should fail the public HTTPS check.'
  );
  assert(
    insecureState.avatarAssetUrlStatusMessage ===
      'Use a public HTTPS GIF URL from Colab; private or local URLs will not load.',
    'Non-HTTPS URLs should produce private URL guidance.'
  );

  context.avatarConfig.avatarAssetUrl = 'https://example.com/avatar.gif';
  const publicState = context.avatarWorkshopValidate();
  assert(
    publicState.avatarAssetUrlIsConfigured === true,
    'Public HTTPS URLs should be treated as configured.'
  );
  assert(
    publicState.avatarAssetUrlIsPublicHttps === true,
    'Public HTTPS URLs should pass the public HTTPS check.'
  );
  assert(
    publicState.avatarAssetUrlStatusMessage === 'Connected to a public avatar URL.',
    'Public HTTPS URLs should confirm the connection state.'
  );

  console.log(
    'CodePen starter validation passed: placeholder fallback, insecure URL rejection, and public HTTPS acceptance.'
  );
}

runValidation();
