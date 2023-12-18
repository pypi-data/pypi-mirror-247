// Generated by the protocol buffer compiler.  DO NOT EDIT!
// source: tensorflow/core/framework/reader_base.proto

#ifndef GOOGLE_PROTOBUF_INCLUDED_tensorflow_2fcore_2fframework_2freader_5fbase_2eproto
#define GOOGLE_PROTOBUF_INCLUDED_tensorflow_2fcore_2fframework_2freader_5fbase_2eproto

#include <limits>
#include <string>

#include <google/protobuf/port_def.inc>
#if PROTOBUF_VERSION < 3021000
#error This file was generated by a newer version of protoc which is
#error incompatible with your Protocol Buffer headers. Please update
#error your headers.
#endif
#if 3021009 < PROTOBUF_MIN_PROTOC_VERSION
#error This file was generated by an older version of protoc which is
#error incompatible with your Protocol Buffer headers. Please
#error regenerate this file with a newer version of protoc.
#endif

#include <google/protobuf/port_undef.inc>
#include <google/protobuf/io/coded_stream.h>
#include <google/protobuf/arena.h>
#include <google/protobuf/arenastring.h>
#include <google/protobuf/generated_message_util.h>
#include <google/protobuf/metadata_lite.h>
#include <google/protobuf/generated_message_reflection.h>
#include <google/protobuf/message.h>
#include <google/protobuf/repeated_field.h>  // IWYU pragma: export
#include <google/protobuf/extension_set.h>  // IWYU pragma: export
#include <google/protobuf/unknown_field_set.h>
// @@protoc_insertion_point(includes)
#include <google/protobuf/port_def.inc>
#define PROTOBUF_INTERNAL_EXPORT_tensorflow_2fcore_2fframework_2freader_5fbase_2eproto
PROTOBUF_NAMESPACE_OPEN
namespace internal {
class AnyMetadata;
}  // namespace internal
PROTOBUF_NAMESPACE_CLOSE

// Internal implementation detail -- do not use these members.
struct TableStruct_tensorflow_2fcore_2fframework_2freader_5fbase_2eproto {
  static const uint32_t offsets[];
};
extern const ::PROTOBUF_NAMESPACE_ID::internal::DescriptorTable descriptor_table_tensorflow_2fcore_2fframework_2freader_5fbase_2eproto;
namespace tensorflow {
class ReaderBaseState;
struct ReaderBaseStateDefaultTypeInternal;
extern ReaderBaseStateDefaultTypeInternal _ReaderBaseState_default_instance_;
}  // namespace tensorflow
PROTOBUF_NAMESPACE_OPEN
template<> ::tensorflow::ReaderBaseState* Arena::CreateMaybeMessage<::tensorflow::ReaderBaseState>(Arena*);
PROTOBUF_NAMESPACE_CLOSE
namespace tensorflow {

// ===================================================================

class ReaderBaseState final :
    public ::PROTOBUF_NAMESPACE_ID::Message /* @@protoc_insertion_point(class_definition:tensorflow.ReaderBaseState) */ {
 public:
  inline ReaderBaseState() : ReaderBaseState(nullptr) {}
  ~ReaderBaseState() override;
  explicit PROTOBUF_CONSTEXPR ReaderBaseState(::PROTOBUF_NAMESPACE_ID::internal::ConstantInitialized);

  ReaderBaseState(const ReaderBaseState& from);
  ReaderBaseState(ReaderBaseState&& from) noexcept
    : ReaderBaseState() {
    *this = ::std::move(from);
  }

  inline ReaderBaseState& operator=(const ReaderBaseState& from) {
    CopyFrom(from);
    return *this;
  }
  inline ReaderBaseState& operator=(ReaderBaseState&& from) noexcept {
    if (this == &from) return *this;
    if (GetOwningArena() == from.GetOwningArena()
  #ifdef PROTOBUF_FORCE_COPY_IN_MOVE
        && GetOwningArena() != nullptr
  #endif  // !PROTOBUF_FORCE_COPY_IN_MOVE
    ) {
      InternalSwap(&from);
    } else {
      CopyFrom(from);
    }
    return *this;
  }

  static const ::PROTOBUF_NAMESPACE_ID::Descriptor* descriptor() {
    return GetDescriptor();
  }
  static const ::PROTOBUF_NAMESPACE_ID::Descriptor* GetDescriptor() {
    return default_instance().GetMetadata().descriptor;
  }
  static const ::PROTOBUF_NAMESPACE_ID::Reflection* GetReflection() {
    return default_instance().GetMetadata().reflection;
  }
  static const ReaderBaseState& default_instance() {
    return *internal_default_instance();
  }
  static inline const ReaderBaseState* internal_default_instance() {
    return reinterpret_cast<const ReaderBaseState*>(
               &_ReaderBaseState_default_instance_);
  }
  static constexpr int kIndexInFileMessages =
    0;

  friend void swap(ReaderBaseState& a, ReaderBaseState& b) {
    a.Swap(&b);
  }
  inline void Swap(ReaderBaseState* other) {
    if (other == this) return;
  #ifdef PROTOBUF_FORCE_COPY_IN_SWAP
    if (GetOwningArena() != nullptr &&
        GetOwningArena() == other->GetOwningArena()) {
   #else  // PROTOBUF_FORCE_COPY_IN_SWAP
    if (GetOwningArena() == other->GetOwningArena()) {
  #endif  // !PROTOBUF_FORCE_COPY_IN_SWAP
      InternalSwap(other);
    } else {
      ::PROTOBUF_NAMESPACE_ID::internal::GenericSwap(this, other);
    }
  }
  void UnsafeArenaSwap(ReaderBaseState* other) {
    if (other == this) return;
    GOOGLE_DCHECK(GetOwningArena() == other->GetOwningArena());
    InternalSwap(other);
  }

  // implements Message ----------------------------------------------

  ReaderBaseState* New(::PROTOBUF_NAMESPACE_ID::Arena* arena = nullptr) const final {
    return CreateMaybeMessage<ReaderBaseState>(arena);
  }
  using ::PROTOBUF_NAMESPACE_ID::Message::CopyFrom;
  void CopyFrom(const ReaderBaseState& from);
  using ::PROTOBUF_NAMESPACE_ID::Message::MergeFrom;
  void MergeFrom( const ReaderBaseState& from) {
    ReaderBaseState::MergeImpl(*this, from);
  }
  private:
  static void MergeImpl(::PROTOBUF_NAMESPACE_ID::Message& to_msg, const ::PROTOBUF_NAMESPACE_ID::Message& from_msg);
  public:
  PROTOBUF_ATTRIBUTE_REINITIALIZES void Clear() final;
  bool IsInitialized() const final;

  size_t ByteSizeLong() const final;
  const char* _InternalParse(const char* ptr, ::PROTOBUF_NAMESPACE_ID::internal::ParseContext* ctx) final;
  uint8_t* _InternalSerialize(
      uint8_t* target, ::PROTOBUF_NAMESPACE_ID::io::EpsCopyOutputStream* stream) const final;
  int GetCachedSize() const final { return _impl_._cached_size_.Get(); }

  private:
  void SharedCtor(::PROTOBUF_NAMESPACE_ID::Arena* arena, bool is_message_owned);
  void SharedDtor();
  void SetCachedSize(int size) const final;
  void InternalSwap(ReaderBaseState* other);

  private:
  friend class ::PROTOBUF_NAMESPACE_ID::internal::AnyMetadata;
  static ::PROTOBUF_NAMESPACE_ID::StringPiece FullMessageName() {
    return "tensorflow.ReaderBaseState";
  }
  protected:
  explicit ReaderBaseState(::PROTOBUF_NAMESPACE_ID::Arena* arena,
                       bool is_message_owned = false);
  public:

  static const ClassData _class_data_;
  const ::PROTOBUF_NAMESPACE_ID::Message::ClassData*GetClassData() const final;

  ::PROTOBUF_NAMESPACE_ID::Metadata GetMetadata() const final;

  // nested types ----------------------------------------------------

  // accessors -------------------------------------------------------

  enum : int {
    kCurrentWorkFieldNumber = 4,
    kWorkStartedFieldNumber = 1,
    kWorkFinishedFieldNumber = 2,
    kNumRecordsProducedFieldNumber = 3,
  };
  // bytes current_work = 4;
  void clear_current_work();
  const std::string& current_work() const;
  template <typename ArgT0 = const std::string&, typename... ArgT>
  void set_current_work(ArgT0&& arg0, ArgT... args);
  std::string* mutable_current_work();
  PROTOBUF_NODISCARD std::string* release_current_work();
  void set_allocated_current_work(std::string* current_work);
  private:
  const std::string& _internal_current_work() const;
  inline PROTOBUF_ALWAYS_INLINE void _internal_set_current_work(const std::string& value);
  std::string* _internal_mutable_current_work();
  public:

  // int64 work_started = 1;
  void clear_work_started();
  int64_t work_started() const;
  void set_work_started(int64_t value);
  private:
  int64_t _internal_work_started() const;
  void _internal_set_work_started(int64_t value);
  public:

  // int64 work_finished = 2;
  void clear_work_finished();
  int64_t work_finished() const;
  void set_work_finished(int64_t value);
  private:
  int64_t _internal_work_finished() const;
  void _internal_set_work_finished(int64_t value);
  public:

  // int64 num_records_produced = 3;
  void clear_num_records_produced();
  int64_t num_records_produced() const;
  void set_num_records_produced(int64_t value);
  private:
  int64_t _internal_num_records_produced() const;
  void _internal_set_num_records_produced(int64_t value);
  public:

  // @@protoc_insertion_point(class_scope:tensorflow.ReaderBaseState)
 private:
  class _Internal;

  template <typename T> friend class ::PROTOBUF_NAMESPACE_ID::Arena::InternalHelper;
  typedef void InternalArenaConstructable_;
  typedef void DestructorSkippable_;
  struct Impl_ {
    ::PROTOBUF_NAMESPACE_ID::internal::ArenaStringPtr current_work_;
    int64_t work_started_;
    int64_t work_finished_;
    int64_t num_records_produced_;
    mutable ::PROTOBUF_NAMESPACE_ID::internal::CachedSize _cached_size_;
  };
  union { Impl_ _impl_; };
  friend struct ::TableStruct_tensorflow_2fcore_2fframework_2freader_5fbase_2eproto;
};
// ===================================================================


// ===================================================================

#ifdef __GNUC__
  #pragma GCC diagnostic push
  #pragma GCC diagnostic ignored "-Wstrict-aliasing"
#endif  // __GNUC__
// ReaderBaseState

// int64 work_started = 1;
inline void ReaderBaseState::clear_work_started() {
  _impl_.work_started_ = int64_t{0};
}
inline int64_t ReaderBaseState::_internal_work_started() const {
  return _impl_.work_started_;
}
inline int64_t ReaderBaseState::work_started() const {
  // @@protoc_insertion_point(field_get:tensorflow.ReaderBaseState.work_started)
  return _internal_work_started();
}
inline void ReaderBaseState::_internal_set_work_started(int64_t value) {
  
  _impl_.work_started_ = value;
}
inline void ReaderBaseState::set_work_started(int64_t value) {
  _internal_set_work_started(value);
  // @@protoc_insertion_point(field_set:tensorflow.ReaderBaseState.work_started)
}

// int64 work_finished = 2;
inline void ReaderBaseState::clear_work_finished() {
  _impl_.work_finished_ = int64_t{0};
}
inline int64_t ReaderBaseState::_internal_work_finished() const {
  return _impl_.work_finished_;
}
inline int64_t ReaderBaseState::work_finished() const {
  // @@protoc_insertion_point(field_get:tensorflow.ReaderBaseState.work_finished)
  return _internal_work_finished();
}
inline void ReaderBaseState::_internal_set_work_finished(int64_t value) {
  
  _impl_.work_finished_ = value;
}
inline void ReaderBaseState::set_work_finished(int64_t value) {
  _internal_set_work_finished(value);
  // @@protoc_insertion_point(field_set:tensorflow.ReaderBaseState.work_finished)
}

// int64 num_records_produced = 3;
inline void ReaderBaseState::clear_num_records_produced() {
  _impl_.num_records_produced_ = int64_t{0};
}
inline int64_t ReaderBaseState::_internal_num_records_produced() const {
  return _impl_.num_records_produced_;
}
inline int64_t ReaderBaseState::num_records_produced() const {
  // @@protoc_insertion_point(field_get:tensorflow.ReaderBaseState.num_records_produced)
  return _internal_num_records_produced();
}
inline void ReaderBaseState::_internal_set_num_records_produced(int64_t value) {
  
  _impl_.num_records_produced_ = value;
}
inline void ReaderBaseState::set_num_records_produced(int64_t value) {
  _internal_set_num_records_produced(value);
  // @@protoc_insertion_point(field_set:tensorflow.ReaderBaseState.num_records_produced)
}

// bytes current_work = 4;
inline void ReaderBaseState::clear_current_work() {
  _impl_.current_work_.ClearToEmpty();
}
inline const std::string& ReaderBaseState::current_work() const {
  // @@protoc_insertion_point(field_get:tensorflow.ReaderBaseState.current_work)
  return _internal_current_work();
}
template <typename ArgT0, typename... ArgT>
inline PROTOBUF_ALWAYS_INLINE
void ReaderBaseState::set_current_work(ArgT0&& arg0, ArgT... args) {
 
 _impl_.current_work_.SetBytes(static_cast<ArgT0 &&>(arg0), args..., GetArenaForAllocation());
  // @@protoc_insertion_point(field_set:tensorflow.ReaderBaseState.current_work)
}
inline std::string* ReaderBaseState::mutable_current_work() {
  std::string* _s = _internal_mutable_current_work();
  // @@protoc_insertion_point(field_mutable:tensorflow.ReaderBaseState.current_work)
  return _s;
}
inline const std::string& ReaderBaseState::_internal_current_work() const {
  return _impl_.current_work_.Get();
}
inline void ReaderBaseState::_internal_set_current_work(const std::string& value) {
  
  _impl_.current_work_.Set(value, GetArenaForAllocation());
}
inline std::string* ReaderBaseState::_internal_mutable_current_work() {
  
  return _impl_.current_work_.Mutable(GetArenaForAllocation());
}
inline std::string* ReaderBaseState::release_current_work() {
  // @@protoc_insertion_point(field_release:tensorflow.ReaderBaseState.current_work)
  return _impl_.current_work_.Release();
}
inline void ReaderBaseState::set_allocated_current_work(std::string* current_work) {
  if (current_work != nullptr) {
    
  } else {
    
  }
  _impl_.current_work_.SetAllocated(current_work, GetArenaForAllocation());
#ifdef PROTOBUF_FORCE_COPY_DEFAULT_STRING
  if (_impl_.current_work_.IsDefault()) {
    _impl_.current_work_.Set("", GetArenaForAllocation());
  }
#endif // PROTOBUF_FORCE_COPY_DEFAULT_STRING
  // @@protoc_insertion_point(field_set_allocated:tensorflow.ReaderBaseState.current_work)
}

#ifdef __GNUC__
  #pragma GCC diagnostic pop
#endif  // __GNUC__

// @@protoc_insertion_point(namespace_scope)

}  // namespace tensorflow

// @@protoc_insertion_point(global_scope)

#include <google/protobuf/port_undef.inc>
#endif  // GOOGLE_PROTOBUF_INCLUDED_GOOGLE_PROTOBUF_INCLUDED_tensorflow_2fcore_2fframework_2freader_5fbase_2eproto
