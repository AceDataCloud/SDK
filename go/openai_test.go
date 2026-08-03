package acedatacloud

import (
	"context"
	"io"
	"net/http"
	"net/http/httptest"
	"strings"
	"testing"
)

func TestOpenAIModels_List(t *testing.T) {
	srv := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		if r.URL.Path != "/openai/models" {
			t.Errorf("unexpected path %s", r.URL.Path)
		}
		w.Header().Set("Content-Type", "application/json")
		_, _ = w.Write([]byte(`{"data":[{"id":"gpt-4o"}]}`))
	}))
	defer srv.Close()

	c, _ := NewClient(WithAPIToken("token"), WithBaseURL(srv.URL))
	res, err := c.OpenAI().Models().List(context.Background())
	if err != nil {
		t.Fatalf("List: %v", err)
	}
	if _, ok := res["data"].([]any); !ok {
		t.Fatalf("bad response: %+v", res)
	}
}

func TestOpenAIAudio_Speech(t *testing.T) {
	srv := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		if r.URL.Path != "/v1/audio/speech" {
			t.Errorf("unexpected path %s", r.URL.Path)
		}
		body, _ := io.ReadAll(r.Body)
		if !strings.Contains(string(body), `"voice":"nova"`) {
			t.Errorf("voice missing from body: %s", body)
		}
		w.Header().Set("Content-Type", "audio/mpeg")
		_, _ = w.Write([]byte("ID3-audio"))
	}))
	defer srv.Close()

	c, _ := NewClient(WithAPIToken("token"), WithBaseURL(srv.URL))
	audio, err := c.OpenAI().Audio().Speech(context.Background(), SpeechRequest{
		Input: "Hello from AceData Cloud.",
		Model: "tts-1-hd",
		Voice: "nova",
	})
	if err != nil {
		t.Fatalf("Speech: %v", err)
	}
	if string(audio) != "ID3-audio" {
		t.Fatalf("bad audio: %q", audio)
	}
}

func TestOpenAIAudio_Transcriptions(t *testing.T) {
	srv := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		if r.URL.Path != "/v1/audio/transcriptions" {
			t.Errorf("unexpected path %s", r.URL.Path)
		}
		if err := r.ParseMultipartForm(1 << 20); err != nil {
			t.Fatalf("ParseMultipartForm: %v", err)
		}
		if r.MultipartForm.File["file"][0].Filename != "sample.mp3" {
			t.Errorf("bad filename: %s", r.MultipartForm.File["file"][0].Filename)
		}
		if r.MultipartForm.Value["model"][0] != "gpt-transcribe" {
			t.Errorf("bad model: %v", r.MultipartForm.Value["model"])
		}
		if r.MultipartForm.Value["timestamp_granularities[]"][0] != "word" {
			t.Errorf("bad granularities: %v", r.MultipartForm.Value["timestamp_granularities[]"])
		}
		w.Header().Set("Content-Type", "application/json")
		_, _ = w.Write([]byte(`{"text":"Hello."}`))
	}))
	defer srv.Close()

	c, _ := NewClient(WithAPIToken("token"), WithBaseURL(srv.URL))
	res, err := c.OpenAI().Audio().Transcriptions().Create(context.Background(), TranscriptionRequest{
		File:                   []byte("fake-audio"),
		Filename:               "sample.mp3",
		Model:                  "gpt-transcribe",
		TimestampGranularities: []string{"word"},
	})
	if err != nil {
		t.Fatalf("Create: %v", err)
	}
	if res["text"] != "Hello." {
		t.Fatalf("bad response: %+v", res)
	}
}

func TestOpenAIAudio_TranscriptionsPlainText(t *testing.T) {
	srv := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, _ *http.Request) {
		w.Header().Set("Content-Type", "text/plain")
		_, _ = w.Write([]byte("Hello there."))
	}))
	defer srv.Close()

	c, _ := NewClient(WithAPIToken("token"), WithBaseURL(srv.URL))
	res, err := c.OpenAI().Audio().Transcriptions().Create(context.Background(), TranscriptionRequest{
		File:           []byte("fake-audio"),
		ResponseFormat: "text",
	})
	if err != nil {
		t.Fatalf("Create: %v", err)
	}
	if res["text"] != "Hello there." {
		t.Fatalf("bad response: %+v", res)
	}
}

func TestOpenAIAudio_TranscriptionsRequiresFile(t *testing.T) {
	c, _ := NewClient(WithAPIToken("token"))
	if _, err := c.OpenAI().Audio().Transcriptions().Create(context.Background(), TranscriptionRequest{}); err == nil {
		t.Fatal("expected an error when File is empty")
	}
}
