package acedatacloud

// Client is the top-level AceDataCloud SDK client.
//
// It exposes domain-specific resource groups via accessor methods,
// mirroring the Python “AceDataCloud“ class and the TypeScript
// “AceDataCloud“ class.
type Client struct {
	transport *transport

	openai   *OpenAIResource
	chat     *ChatResource
	images   *ImagesResource
	tasks    *TasksResource
	video    *VideoResource
	audio    *AudioResource
	search   *SearchResource
	face     *FaceResource
	shorturl *ShortURLResource
}

// NewClient constructs a Client. At least one of WithAPIToken /
// ACEDATACLOUD_API_TOKEN env var / WithPaymentHandler must be provided.
func NewClient(opts ...Option) (*Client, error) {
	o := defaultOptions()
	for _, fn := range opts {
		fn(o)
	}
	tr, err := newTransport(o)
	if err != nil {
		return nil, err
	}
	c := &Client{transport: tr}
	c.openai = &OpenAIResource{t: tr}
	c.chat = &ChatResource{t: tr}
	c.images = &ImagesResource{t: tr}
	c.tasks = &TasksResource{t: tr}
	c.video = &VideoResource{t: tr}
	c.audio = &AudioResource{t: tr}
	c.search = &SearchResource{t: tr}
	c.face = &FaceResource{t: tr}
	c.shorturl = &ShortURLResource{t: tr}
	return c, nil
}

// OpenAI returns the OpenAI-compatible resource (“/v1/chat/completions“,
// “/openai/responses“).
func (c *Client) OpenAI() *OpenAIResource { return c.openai }

// Chat returns the native chat resource (“/v1/messages“ — Anthropic
// Messages API shape).
func (c *Client) Chat() *ChatResource { return c.chat }

// Images returns the image generation resource.
func (c *Client) Images() *ImagesResource { return c.images }

// Tasks returns the cross-service task retrieval resource.
func (c *Client) Tasks() *TasksResource { return c.tasks }

// Video returns the video-generation resource.
func (c *Client) Video() *VideoResource { return c.video }

// Audio returns the audio/music generation resource.
func (c *Client) Audio() *AudioResource { return c.audio }

// Search returns the web search resource.
func (c *Client) Search() *SearchResource { return c.search }

// Face returns the face transformation resource.
func (c *Client) Face() *FaceResource { return c.face }

// ShortURL returns the short URL resource.
func (c *Client) ShortURL() *ShortURLResource { return c.shorturl }
