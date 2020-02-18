import traceback

class Visualizer: 
    def add_stream_processor(self, sp):
        self.stream_processor_ = sp
        return self

    def add_input_source(self, input_source):
        self.input_source_ = input_source
        return self

    def add_output_source(self, output_source):
        self.output_source_ = output_source 
        return self

    def run(self):
        self.stream_processor_.add_input_stream(self.input_source_)
        
        try:
            while True:
                raw_data = self.input_source_.get_chunk()
                self.stream_processor_.preprocess(raw_data)
                r, g, b = self.stream_processor_.process(raw_data)
                self.output_source_.display(r, g, b)

        except KeyboardInterrupt:
            self.output_source_.shutdown()
        except Exception as e:
            print(e)
            print(traceback.format_exc())
            pass

    