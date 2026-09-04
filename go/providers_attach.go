// Code generated from the platform OpenAPI spec. DO NOT EDIT.
// Regenerate with: python scripts/generate_providers.py

package acedatacloud

// taskIDFrom pulls a task id out of a submission response.
func taskIDFrom(result map[string]any) string {
	if s, ok := result["task_id"].(string); ok && s != "" {
		return s
	}
	if data, ok := result["data"].(map[string]any); ok {
		if s, ok := data["task_id"].(string); ok && s != "" {
			return s
		}
	}
	if s, ok := result["id"].(string); ok {
		return s
	}
	return ""
}

// providers holds the provider-axis clients, one per service.
type providers struct {
	digitalhuman *Digitalhuman
	dreamina     *Dreamina
	fish         *Fish
	flux         *Flux
	gemini       *Gemini
	hailuo       *Hailuo
	happyhorse   *Happyhorse
	localization *Localization
	luma         *Luma
	maestro      *Maestro
	minimax      *Minimax
	nanobanana   *NanoBanana
	producer     *Producer
	qwenimage    *QwenImage
	seedance     *Seedance
	seedream     *Seedream
	suno         *Suno
	wan          *Wan
}

func newProviders(tr *transport) *providers {
	return &providers{
		digitalhuman: &Digitalhuman{t: tr},
		dreamina:     &Dreamina{t: tr},
		fish:         &Fish{t: tr},
		flux:         &Flux{t: tr},
		gemini:       &Gemini{t: tr},
		hailuo:       &Hailuo{t: tr},
		happyhorse:   &Happyhorse{t: tr},
		localization: &Localization{t: tr},
		luma:         &Luma{t: tr},
		maestro:      &Maestro{t: tr},
		minimax:      &Minimax{t: tr},
		nanobanana:   &NanoBanana{t: tr},
		producer:     &Producer{t: tr},
		qwenimage:    &QwenImage{t: tr},
		seedance:     &Seedance{t: tr},
		seedream:     &Seedream{t: tr},
		suno:         &Suno{t: tr},
		wan:          &Wan{t: tr},
	}
}

// Digitalhuman returns the digitalhuman provider client.
func (c *Client) Digitalhuman() *Digitalhuman { return c.providers.digitalhuman }

// Dreamina returns the dreamina provider client.
func (c *Client) Dreamina() *Dreamina { return c.providers.dreamina }

// Fish returns the fish provider client.
func (c *Client) Fish() *Fish { return c.providers.fish }

// Flux returns the flux provider client.
func (c *Client) Flux() *Flux { return c.providers.flux }

// Gemini returns the gemini provider client.
func (c *Client) Gemini() *Gemini { return c.providers.gemini }

// Hailuo returns the hailuo provider client.
func (c *Client) Hailuo() *Hailuo { return c.providers.hailuo }

// Happyhorse returns the happyhorse provider client.
func (c *Client) Happyhorse() *Happyhorse { return c.providers.happyhorse }

// Localization returns the localization provider client.
func (c *Client) Localization() *Localization { return c.providers.localization }

// Luma returns the luma provider client.
func (c *Client) Luma() *Luma { return c.providers.luma }

// Maestro returns the maestro provider client.
func (c *Client) Maestro() *Maestro { return c.providers.maestro }

// Minimax returns the minimax provider client.
func (c *Client) Minimax() *Minimax { return c.providers.minimax }

// NanoBanana returns the nano-banana provider client.
func (c *Client) NanoBanana() *NanoBanana { return c.providers.nanobanana }

// Producer returns the producer provider client.
func (c *Client) Producer() *Producer { return c.providers.producer }

// QwenImage returns the qwen-image provider client.
func (c *Client) QwenImage() *QwenImage { return c.providers.qwenimage }

// Seedance returns the seedance provider client.
func (c *Client) Seedance() *Seedance { return c.providers.seedance }

// Seedream returns the seedream provider client.
func (c *Client) Seedream() *Seedream { return c.providers.seedream }

// Suno returns the suno provider client.
func (c *Client) Suno() *Suno { return c.providers.suno }

// Wan returns the wan provider client.
func (c *Client) Wan() *Wan { return c.providers.wan }
