<?php

namespace App\Livewire;

use Livewire\Component;
use Illuminate\Support\Facades\Http;

class Chatbot extends Component
{
    public $currentMessage = '';
    public $userPrompt = '';
    public $chatMessages = [];

    protected $rules = [
        'currentMessage' => 'required'
    ];

    protected $messages = [
        'currentMessage.required' => 'Please enter a message'
    ];

    public function ask()
    {
        $this->validate();

        $this->chatMessages[] = [
            'type' => 'human',
            'content' => $this->currentMessage
        ];

        $this->userPrompt = $this->currentMessage;
        $this->currentMessage = '';

        $this->generateResponse();
    }

    public function generateResponse()
{
    set_time_limit(120);

    try {
        $response = Http::timeout(120)->post(
            "http://127.0.0.1:8000/chat/travel-agent",
            ['messages' => $this->chatMessages]
        );

        if ($response->status() === 503) {
            $this->chatMessages[] = [
                'type' => 'ai',
                'content' => "⚠️ Servizio temporaneamente non disponibile. Riprova."
            ];
            return;
        }

        if (!$response->successful()) {
            $this->chatMessages[] = [
                'type' => 'ai',
                'content' => "⚠️ Errore dal server: " . $response->status()
            ];
            return;
        }

        $data = $response->json();


        if (isset($data['content'])) {
            $this->chatMessages[] = [
                'type' => 'ai',
                'content' => $data['content']
            ];
        } else {
            // Debug temporaneo — rimuovi dopo aver verificato
            $this->chatMessages[] = [
                'type' => 'ai',
                'content' => "⚠️ Risposta inattesa: " . json_encode($data)
            ];
        }

    } catch (\Illuminate\Http\Client\ConnectionException $e) {
        $this->chatMessages[] = [
            'type' => 'ai',
            'content' => "⚠️ Il server ha impiegato troppo tempo. Riprova."
        ];
    }
}

    public function render()
    {
        $this->dispatch('scrollChatToBottom');
        return view('livewire.chatbot');
    }
}